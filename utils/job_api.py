"""
Job API integration layer for querying recruitment opportunities via Adzuna API.
"""
import requests  # type: ignore
import streamlit as st
import logging

# Configure logger for HireReady
logger = logging.getLogger("HireReady")

@st.cache_data(ttl=300)
def fetch_jobs(role: str, location: str, job_type: str) -> list:
    """
    Fetches job listings from Adzuna Jobs API for India across 7 pages,
    applies relaxed role matching, expanded internship detection,
    and logs detailed diagnostic statistics.

    Args:
        role (str): Role keyword (e.g. "Developer", "Analyst").
        location (str): Selected target city from pre-defined list.
        job_type (str): "Internship" or "Full-Time".

    Returns:
        list: Normalized job details.
    """
    # Log search parameters
    logger.info(f"--- Adzuna Search Quality Audit ---")
    logger.info(f"Parameters: role='{role}', location='{location}', job_type='{job_type}'")

    # Get credentials from Streamlit secrets
    try:
        app_id = st.secrets["ADZUNA_APP_ID"]
        app_key = st.secrets["ADZUNA_APP_KEY"]
    except KeyError:
        raise ValueError("Invalid credentials: ADZUNA_APP_ID or ADZUNA_APP_KEY not configured in .streamlit/secrets.toml")

    if app_id in ("dummy_app_id", "") or app_key in ("dummy_app_key", ""):
        raise ValueError("Invalid credentials: Adzuna API credentials in secrets.toml are placeholders. Please configure valid credentials.")

    jobs_list = []
    role_query = role.strip().lower()
    
    total_jobs_from_api = 0
    after_role_filter = 0
    after_job_type_filter = 0
    
    raw_titles = []
    
    # We query pages 1 to 7 to maximize discovery
    for page in range(1, 8):
        base_url = f"https://api.adzuna.com/v1/api/jobs/in/search/{page}"
        
        params = {
            "app_id": app_id,
            "app_key": app_key,
            "content-type": "application/json",
            "results_per_page": 20
        }
        
        if role_query:
            params["what"] = role.strip()
        if location.strip():
            params["where"] = location.strip()

        try:
            response = requests.get(base_url, params=params, timeout=10)
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Network failure on page {page}: {str(e)}")

        if response.status_code in (401, 403):
            raise ValueError("Invalid credentials: App ID or App Key is unauthorized or incorrect.")
        elif response.status_code == 429:
            raise ValueError("Rate limits exceeded: Adzuna API request limit reached.")
        elif response.status_code != 200:
            raise ValueError(f"API Error on page {page}: Status Code {response.status_code}")

        try:
            data = response.json()
        except Exception:
            raise ValueError(f"Malformed response on page {page}: not valid JSON.")

        results = data.get("results", [])
        if not results:
            break  # No more results available
            
        for item in results:
            total_jobs_from_api += 1
            title = item.get("title", "")
            clean_title = title.replace("<strong>", "").replace("</strong>", "")
            
            # Record first 20 titles before filtering
            if len(raw_titles) < 20:
                raw_titles.append(clean_title)
                
            company_info = item.get("company", {})
            company_name = company_info.get("display_name", "Unknown Company")
            apply_url = item.get("redirect_url", "#")
            latitude = item.get("latitude")
            longitude = item.get("longitude")
            
            loc_info = item.get("location", {})
            location_display = loc_info.get("display_name", "")
            
            # 1. Relaxed Role Match Check
            if not role_query:
                role_match = True
            else:
                role_tokens = [t for t in role_query.split() if len(t) > 2]
                if not role_tokens:
                    role_match = (role_query in clean_title.lower())
                else:
                    role_match = any(token in clean_title.lower() for token in role_tokens)
            
            if not role_match:
                continue
            after_role_filter += 1
            
            # 2. Expanded Internship / Job Type Detection
            internship_keywords = [
                "intern", "internship", "trainee", "graduate trainee", 
                "apprentice", "student", "campus", "associate intern"
            ]
            is_internship = any(kw in clean_title.lower() for kw in internship_keywords)
            mapped_type = "Internship" if is_internship else "Full-Time"
            
            type_match = (job_type == mapped_type)
            if not type_match:
                continue
            after_job_type_filter += 1
            
            # Add to matching list (no local location filtering is applied)
            jobs_list.append({
                "company": company_name,
                "role": clean_title,
                "location": location_display if location_display else location,
                "job_type": mapped_type,
                "apply_url": apply_url,
                "latitude": float(latitude) if latitude is not None else None,
                "longitude": float(longitude) if longitude is not None else None
            })

    # Log diagnostics in console logs
    logger.info(f"Raw titles before filtering (up to 20):")
    for idx, t in enumerate(raw_titles, 1):
        logger.info(f"  {idx}. {t}")
        
    logger.info(f"Diagnostic Metrics:")
    logger.info(f"  - Total jobs from API: {total_jobs_from_api}")
    logger.info(f"  - Jobs after role filtering: {after_role_filter}")
    logger.info(f"  - Jobs after job type filtering: {after_job_type_filter}")
    logger.info(f"  - Final displayed jobs: {len(jobs_list)}")

    return jobs_list
