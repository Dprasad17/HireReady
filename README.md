# HireReady - Placement Readiness Intelligence Dashboard

HireReady is a Placement Readiness Intelligence Dashboard designed to help students track their preparation activities, analyze progress, explore live career opportunities, and compile recruiter-ready performance reports.

---

## 🚀 Project Overview
In competitive campus recruitment environments, preparation is often fragmented. Students practice coding on external platforms, track projects locally, and search for openings across multiple job boards. **HireReady** addresses this by unifying these key pillars into a cohesive career cockpit. Evaluators and recruiters can instantly review the student's compiled **Placement Readiness Index**.

---

## ✨ Key Features
- **🔑 Persistent User Profile System**: Log in with an email address to load and save preparation data across sessions, browser refreshes, or server restarts.
- **📊 Interactive Readiness Dashboard**: Monitor unified preparation indicators (DSA Solved, Mock Interview Scores, Job Applications, Projects) calculated out of a 100-point composite Readiness Score.
- **📝 Progress Tracking Center**: Log daily coding sheets, mock scores, and projects via validated Streamlit forms.
- **💼 Live Opportunities Explorer**: Retrieve active postings using the Adzuna Jobs API filtered by keywords and cities in India.
- **📍 Interactive Maps**: Plot openings on a Folium map using coordinates centered on India or search cities.
- **💾 Data Ingestion & Export Hub**: Import preparation logs from user-uploaded CSV/Excel sheets and download filtered data or structured TXT placement reports with rule-based recommendations.

---

## 👤 User Profile System Architecture

### 1. Storage Structure
* **User Data Directory**: `data/users/`
* **CSV Datasets**: Each user has a unique CSV file named after their sanitized email address (e.g., `data/users/durga_gmail_com.csv`).
* **Metadata Profile Register**: `data/users/profiles.json` persists mapping of user email addresses to their display names.

### 2. User Flows
* **First-Time User**:
  - Enter Full Name and Email Address.
  - The system creates a user-specific CSV initialized with the locked HireReady schema and updates `data/users/profiles.json`.
  - Redirects to the Dashboard.
* **Returning User**:
  - Enter Email Address (and Name, though email is the unique key).
  - The system checks if the sanitized CSV file exists, restores records to Streamlit session state, retrieves their display name from `profiles.json`, and loads the Dashboard.

### 3. Sidebar controls
* **Logout**: Clears active session states and redirects to the Login screen. The user's CSV file and history on disk are preserved.
* **Reset Dataset**: Truncates both the memory dataframe and the CSV file on disk to an empty state with columns.

---

## 🛠️ Technology Stack
- **Core**: Python 3.11+, Streamlit
- **Data Engineering**: Pandas, NumPy, OpenPyXL
- **Visualization**: Plotly Express
- **Geospatial Mapping**: Folium, Streamlit-Folium
- **Network Queries**: Requests API
- **Branded Design**: Streamlit Custom Theme (Blue/Green Palette)

---

## 📂 Folder Structure
```
HireReady/
│
├── .streamlit/
│   ├── config.toml            # Styled career-themed colors (Blue, Green, White)
│   └── secrets.toml           # Local API keys (ADZUNA_APP_ID, ADZUNA_APP_KEY)
│
├── assets/
│   └── logo.png               # Minimalist branding icon (Corporate Arrow/Briefcase)
│
├── data/
│   └── users/                 # Persistent CSV files & profiles.json metadata
│
├── pages/                     # Multipage Streamlit layouts
│   ├── 0_Login.py             # User Login and profile initialization
│   ├── 1_Dashboard.py         # KPIs and Analytics Dashboard view
│   ├── 2_Job_Explorer.py      # Map job postings layout
│   ├── 3_Progress_Tracker.py  # Student checklist input layout
│   └── 4_Import_Export.py     # CSV/Excel Data importing/exporting options
│
├── utils/                     # Utility libraries and API logic
│   ├── __init__.py            # Export module loaders
│   ├── config.py              # Configuration constants
│   ├── chart_utils.py         # Plotly rendering and data aggregation
│   ├── data_utils.py          # Data ingestion and validation helpers
│   ├── job_api.py             # Public jobs API fetcher (Adzuna API)
│   ├── kpi_utils.py           # KPIs indicators and scoring algorithms
│   ├── map_utils.py           # Predefined coordinates list and folium canvas builders
│   ├── session_manager.py     # Session State manager
│   └── ui_utils.py            # Reusable header, footer, empty-state, and logo components
│
├── app.py                     # Main router and configurations
├── requirements.txt           # Main dependencies
├── README.md                  # Detailed project documentation
└── .gitignore                 # Version control ignore lists
```

---

## ⚙️ Application Workflow Diagram
```
User Enters Email and Name (Login Page)
│
▼
Navigator Authenticates Profile (app.py Routing)
│
▼
Dashboard & Sidebar Card Displays User Metadata (Last Saved, Records)
│
▼
Progress Tracking Center (Adds entries -> Auto-saves user CSV on disk)
│
▼
Import / Export Ingestion (Uploads new dataset -> Overwrites user CSV on disk)
│
▼
Logout (Clears session -> Redirects to Login screen; preserves files)
```

---

## 📦 Setup & Installation Instructions

### Prerequisites
- Python 3.8 or higher.
- `pip` package installer.

### Steps
1. Clone this repository to your local directory.
2. Navigate to the project directory:
   ```bash
   cd HireReady
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure `.streamlit/secrets.toml` with your Adzuna App ID and Key:
   ```toml
   ADZUNA_APP_ID = "your_app_id"
   ADZUNA_APP_KEY = "your_app_key"
   ```
5. Start the application:
   ```bash
   streamlit run app.py
   ```
6. Open your browser and navigate to `http://localhost:8501`.
