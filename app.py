import streamlit as st
import pandas as pd
import plotly.express as px
from supabase import create_client, Client
from dotenv import load_dotenv
import os

# Page configuration - MUST be first Streamlit command
st.set_page_config(
    page_title="Water Quality Dashboard",
    page_icon="💧",
    layout="wide"
)

# Load environment variables
load_dotenv()

# Initialize Supabase
@st.cache_resource
def init_supabase():
    url = st.secrets.supabase_url
    key = st.secrets.supabase_key
    return create_client(url, key)

supabase = init_supabase()

def login():
    """Handle user login"""
    st.title("🔐 Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        try:
            user = supabase.auth.sign_in_with_password({"email": email, "password": password})
            st.session_state['user'] = user
            st.rerun()
        except Exception as e:
            st.error("Login failed. Please check your credentials.")
    
    if st.button("Create Account"):
        st.session_state['show_signup'] = True
        st.rerun()

def signup():
    """Handle user signup"""
    st.title("Create Account")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    
    if st.button("Sign Up"):
        if password != confirm_password:
            st.error("Passwords don't match!")
            return
        try:
            user = supabase.auth.sign_up({"email": email, "password": password})
            st.success("Account created successfully! Please login.")
            st.session_state['show_signup'] = False
            st.rerun()
        except Exception as e:
            st.error(f"Error creating account: {str(e)}")
    
    if st.button("Back to Login"):
        st.session_state['show_signup'] = False
        st.rerun()

def view_data():
    """Public data view for volunteers"""
    st.header("Water Quality Data")
    # Fetch and display data
    try:
        response = supabase.table('water_quality').select("*").order('date').execute()
        df = pd.DataFrame(response.data)
        
        if not df.empty:
            # Convert date column to datetime
            df['date'] = pd.to_datetime(df['date'])
            
            # Display data table
            st.subheader("Raw Data")
            st.dataframe(df, use_container_width=True)
            
            # Create visualizations for each parameter
            st.header("Water Quality Metrics Over Time")
            
            # Define the parameters to plot
            parameters = [
                ('dissolved_oxygen_mg', 'Dissolved Oxygen (mg/L)'),
                ('dissolved_oxygen_sat', 'Dissolved Oxygen (% saturation)'),
                ('hardness', 'Hardness (mg/L CaCO3)'),
                ('alkalinity', 'Alkalinity (mg/L CaCO3)'),
                ('ph', 'pH (S.U.s)'),
                ('temperature', 'Temperature'),
                ('flow', 'Flow')
            ]
            
            # Create a line chart for each parameter showing all three sites
            for param_col, param_title in parameters:
                if param_col in df.columns:
                    fig = px.line(df, x='date', y=param_col, color='site', 
                                title=f'{param_title} - All Sites',
                                labels={'date': 'Date', param_col: param_title, 'site': 'Site'})
                    fig.update_layout(height=400)
                    st.plotly_chart(fig, use_container_width=True)
                
        else:
            st.info("No water quality data available.")
            
    except Exception as e:
        st.error(f"Error fetching data: {str(e)}")

def dashboard():
    """Main dashboard view for authenticated users"""
    st.title("💧 Water Quality Monitoring Dashboard")
    
    # Navigation
    tab1, tab2 = st.tabs(["📊 View Data", "➕ Add New Data"])
    
    with tab1:
        view_data()
    
    with tab2:
        st.header("Add New Water Quality Data")
        with st.form("water_quality_form"):
            # Site selection
            site = st.selectbox("Site", ["Site 1", "Site 2", "Site 3"])
            date = st.date_input("Date")
            
            col1, col2 = st.columns(2)
            
            with col1:
                dissolved_oxygen_mg = st.number_input("Dissolved Oxygen (mg/L)", min_value=0.0, format="%.2f")
                dissolved_oxygen_sat = st.number_input("Dissolved Oxygen (% saturation)", min_value=0.0, max_value=200.0, format="%.1f")
                hardness = st.number_input("Hardness (mg/L CaCO3)", min_value=0.0, format="%.1f")
                alkalinity = st.number_input("Alkalinity (mg/L CaCO3)", min_value=0.0, format="%.1f")
                
            with col2:
                ph = st.number_input("pH (S.U.s)", min_value=0.0, max_value=14.0, step=0.1, format="%.1f")
                temperature = st.number_input("Temperature", format="%.1f")
                flow = st.number_input("Flow", format="%.2f")
                notes = st.text_area("Notes")
            
            if st.form_submit_button("Submit Data"):
                try:
                    data = {
                        'site': site,
                        'date': str(date),
                        'dissolved_oxygen_mg': dissolved_oxygen_mg,
                        'dissolved_oxygen_sat': dissolved_oxygen_sat,
                        'hardness': hardness,
                        'alkalinity': alkalinity,
                        'ph': ph,
                        'temperature': temperature,
                        'flow': flow,
                        'notes': notes,
                        'user_id': st.session_state['user'].user.id
                    }
                    
                    supabase.table('water_quality').insert(data).execute()
                    st.success("Data submitted successfully!")
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"Error submitting data: {str(e)}")
    
    # Logout button
    if st.sidebar.button("Logout"):
        if 'user' in st.session_state:
            del st.session_state['user']
        st.rerun()

# Main app logic
if 'user' not in st.session_state:
    # Show public view with login option in sidebar
    st.title("💧 Water Quality Monitoring Dashboard")
    
    # Sidebar for login/signup
    with st.sidebar:
        st.header("🔐 Login")
        
        # Initialize show_signup if it doesn't exist
        if 'show_signup' not in st.session_state:
            st.session_state['show_signup'] = False
        
        if st.session_state['show_signup']:
            st.subheader("Create Account")
            email = st.text_input("Email", key="signup_email")
            password = st.text_input("Password", type="password", key="signup_password")
            confirm_password = st.text_input("Confirm Password", type="password", key="signup_confirm")
            
            if st.button("Sign Up"):
                if password != confirm_password:
                    st.error("Passwords don't match!")
                else:
                    try:
                        user = supabase.auth.sign_up({"email": email, "password": password})
                        st.success("Account created! Please login.")
                        st.session_state['show_signup'] = False
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error creating account: {str(e)}")
            
            if st.button("Back to Login"):
                st.session_state['show_signup'] = False
                st.rerun()
        else:
            email = st.text_input("Email", key="login_email")
            password = st.text_input("Password", type="password", key="login_password")
            
            if st.button("Login"):
                try:
                    user = supabase.auth.sign_in_with_password({"email": email, "password": password})
                    st.session_state['user'] = user
                    st.rerun()
                except Exception as e:
                    st.error("Login failed. Please check your credentials.")
            
            if st.button("Create Account"):
                st.session_state['show_signup'] = True
                st.rerun()
        
        st.markdown("---")
        st.info("💡 **Volunteers**: You can view all water quality data without logging in!")
    
    # Show public data view
    view_data()
else:
    dashboard()
