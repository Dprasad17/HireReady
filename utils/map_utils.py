"""
Geospatial mapping utility functions using Folium.
"""
import folium

# Predefined city coordinate mapping (Indian hiring hubs only)
CITY_COORDINATES = {
    "Bangalore": [12.9716, 77.5946],
    "Hyderabad": [17.3850, 78.4867],
    "Chennai": [13.0827, 80.2707],
    "Mumbai": [19.0760, 72.8777],
    "Pune": [18.5204, 73.8567],
    "Delhi": [28.6139, 77.2090],
    "Noida": [28.5355, 77.3910],
    "Gurugram": [28.4595, 77.0266],
    "Kolkata": [22.5726, 88.3639],
    "Ahmedabad": [23.0225, 72.5714],
    "Kochi": [9.9312, 76.2673]
}

# India default coordinates when no search is active
DEFAULT_CENTER = [20.5937, 78.9629]

def create_job_map(job_data: list, center_coords: list) -> folium.Map:
    """
    Creates an interactive Folium Map centered on the target coordinate and plots matching job markers.

    Args:
        job_data (list): Collection of parsed job listings.
        center_coords (list): [latitude, longitude] center coordinates of the map.

    Returns:
        folium.Map: Completed folium map object.
    """
    zoom_val = 5 if center_coords == DEFAULT_CENTER else 11
    
    # Initialize Folium Map
    m = folium.Map(
        location=center_coords,
        zoom_start=zoom_val,
        control_scale=True
    )
    
    # Iterate and place markers
    for job in job_data:
        loc_str = job.get("location", "")
        lat = job.get("latitude")
        lon = job.get("longitude")
        
        # Locate matching city coordinates
        coords = None
        if lat is not None and lon is not None:
            try:
                coords = [float(lat), float(lon)]
            except (ValueError, TypeError):
                coords = None
                
        if not coords:
            for city, city_coords in CITY_COORDINATES.items():
                if city.lower() in loc_str.lower():
                    coords = city_coords
                    break
                
        if coords:
            popup_html = f"""
            <div style="font-family: sans-serif; font-size: 0.9em;">
                <b>🏢 Company:</b> {job.get('company')}<br>
                <b>🎯 Role:</b> {job.get('role')}<br>
                <b>📍 Location:</b> {job.get('location')}<br>
                <a href="{job.get('apply_url')}" target="_blank" style="color: #1E3A8A; font-weight: bold; text-decoration: none;">Apply Here</a>
            </div>
            """
            
            folium.Marker(
                location=coords,
                popup=folium.Popup(popup_html, max_width=300),
                tooltip=f"{job.get('company')} - {job.get('role')}"
            ).add_to(m)
            
    return m
