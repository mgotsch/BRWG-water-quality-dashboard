import streamlit as st
import pandas as pd
from supabase import create_client, Client
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def init_supabase():
    """Initialize Supabase client"""
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    return create_client(url, key)

def site_information():
    """Display detailed site information including coordinates and descriptions"""
    st.header("📍 Site Information")
    st.markdown("*Detailed information about Blue River Watershed Group monitoring locations*")
    
    # Load sites from database
    try:
        supabase = init_supabase()
        response = supabase.table('sites').select("*").order('site_number').execute()
        sites_from_db = response.data
        
        # Convert to DataFrame format
        sites_data = {
            'Site Name': [site['full_name'] for site in sites_from_db],
            'Site Number': [site['site_number'] for site in sites_from_db],
            'Short Name': [site['short_name'] for site in sites_from_db],
            'Latitude': [float(site['latitude']) for site in sites_from_db],
            'Longitude': [float(site['longitude']) for site in sites_from_db],
            'Description': [site['description'] for site in sites_from_db],
            'Elevation (ft)': [site['elevation'] for site in sites_from_db]
        }
        
        df_sites = pd.DataFrame(sites_data)
        
    except Exception as e:
        st.error(f"Error loading sites from database: {str(e)}")
        # Fallback to hardcoded data if database fails
        sites_data = {
            'Site Name': [
                'Blue River at Silverthorne Pavilion- 196',
                'Snake River KSS- 52', 
                'Swan River Reach A- 1007'
            ],
            'Site Number': [
                196,
                52,
                1007
            ],
            'Short Name': [
                'Blue River',
                'Snake River',
                'Swan River'
            ],
            'Latitude': [
                39.6297,
                39.6123,
                39.6445
            ],
            'Longitude': [
                -106.0711,
                -106.0856,
                -106.0789
            ],
            'Description': [
                'Located at Silverthorne Pavilion, this site monitors the Blue River as it flows through the town of Silverthorne.',
                'Monitoring location on the Snake River at Keystone Science School, providing data on this important tributary.',
                'Swan River monitoring site in Reach A, tracking water quality in this scenic mountain watershed.'
            ],
            'Elevation (ft)': [
                9035,
                9150,
                9200
            ]
        }
        
        df_sites = pd.DataFrame(sites_data)
    
    # Display each site in a separate container
    for idx, row in df_sites.iterrows():
        with st.container():
            st.subheader(f"🏔️ {row['Short Name']}")
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.write(f"**Site Number:** {row['Site Number']}")
                st.write(f"**Full Name:** {row['Site Name']}")
                st.write(f"**Description:** {row['Description']}")
                st.write(f"**Coordinates:** {row['Latitude']:.4f}°N, {abs(row['Longitude']):.4f}°W")
                st.write(f"**Elevation:** {row['Elevation (ft)']} feet")
            
            with col2:
                # Create a simple map for each site
                site_map_data = pd.DataFrame({
                    'lat': [row['Latitude']],
                    'lon': [row['Longitude']]
                })
                st.map(site_map_data, zoom=12)
            
            st.markdown("---")
    
    # Summary map with all sites
    st.subheader("🗺️ All Monitoring Sites")
    st.markdown("*Overview map showing all Blue River Watershed Group monitoring locations*")
    
    # Create map data for all sites
    map_data = pd.DataFrame({
        'lat': df_sites['Latitude'],
        'lon': df_sites['Longitude'],
        'site': df_sites['Short Name']
    })
    
    st.map(map_data, zoom=11)
    
    # Additional information
    st.markdown("---")
    st.subheader("ℹ️ About Our Monitoring Program")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Monitoring Parameters:**
        - Dissolved Oxygen (mg/L and % saturation)
        - Water Temperature (°C)
        - pH (Standard Units)
        - Hardness (mg/L CaCO₃)
        - Alkalinity (mg/L CaCO₃)
        - Stream Flow (cfs)
        """)
    
    with col2:
        st.markdown("""
        **Data Collection:**
        - Citizen Scientists trained in CPW River Watch protocols
        - Regular monthly sampling schedule
        - Quality assured data following state standards
        - Contributing to Colorado's water quality database
        """)
    
    st.info("💡 **Want to get involved?** Contact the Blue River Watershed Group to learn about volunteer opportunities for water quality monitoring!")
