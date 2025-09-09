# Water Quality Monitoring Dashboard

A web-based dashboard for monitoring water quality parameters with user authentication and data visualization.

## Features

- User authentication (sign up and login)
- Input water quality data (pH, temperature, dissolved oxygen, turbidity, etc.)
- View data in tabular format
- Interactive charts for data visualization
- Secure data storage with Supabase
- Responsive design for all devices

## Prerequisites

- Python 3.8+
- Supabase account

## Setup Instructions

1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Set up your Supabase project:
   - Go to [Supabase](https://supabase.com/) and create a new project
   - Create a table called `water_quality` with the following columns:
     - id (uuid, primary key, default: `gen_random_uuid()`)
     - site (text) - Site 1, Site 2, or Site 3
     - date (date)
     - dissolved_oxygen_mg (float8) - Dissolved Oxygen (mg/L)
     - dissolved_oxygen_sat (float8) - Dissolved Oxygen (% saturation)
     - hardness (float8) - Hardness (mg/L CaCO3)
     - alkalinity (float8) - Alkalinity (mg/L CaCO3)
     - ph (float8) - pH (S.U.s)
     - temperature (float8) - Temperature
     - flow (float8) - Flow
     - notes (text)
     - user_id (uuid, references auth.users)
     - created_at (timestamp with time zone, default: now())
   - Enable Row Level Security (RLS) on the table
   - Create a policy to allow authenticated users to read all data and insert their own data

4. Configure environment variables:
   - Copy `.env.example` to `.env`
   - Update the Supabase URL and anon key in the `.env` file

## Running the Application

1. Start the Streamlit app:
   ```
   streamlit run app.py
   ```
2. Open your browser and go to `http://localhost:8501`

## Usage

1. Create an account or log in if you already have one
2. Navigate between the "View Data" and "Add New Data" tabs
3. Add new water quality measurements using the form
4. View the data table and interactive charts

## License

This project is licensed under the MIT License.
