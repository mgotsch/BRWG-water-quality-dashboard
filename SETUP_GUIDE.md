# Supabase Setup Guide for Water Quality Dashboard

Follow these steps to set up your Supabase database:

## Step 1: Create Supabase Project

1. Go to [supabase.com](https://supabase.com/)
2. Click "Start your project"
3. Sign up or log in with your account
4. Click "New Project"
5. Choose your organization
6. Fill in project details:
   - Name: "Water Quality Monitor" (or your preferred name)
   - Database Password: Create a strong password (save this!)
   - Region: Choose closest to your location
7. Click "Create new project"
8. Wait for the project to be created (takes 1-2 minutes)

## Step 2: Set Up the Database

1. In your Supabase dashboard, click on "SQL Editor" in the left sidebar
2. Click "New query"
3. Copy and paste the entire contents of `setup_database.sql` into the editor
4. Click "Run" to execute the SQL commands
5. You should see "Success. No rows returned" - this means it worked!

## Step 3: Get Your Project Credentials

1. Go to "Settings" → "API" in your Supabase dashboard
2. Copy the following values:
   - **Project URL** (looks like: `https://your-project-id.supabase.co`)
   - **anon public** key (the long string under "Project API keys")

## Step 4: Configure Environment Variables

1. Open the `.env` file in your project
2. Replace the placeholder values:
   ```
   SUPABASE_URL=https://your-project-id.supabase.co
   SUPABASE_KEY=your-anon-public-key-here
   ```

## Step 5: Install Dependencies and Run

1. Open terminal in your project directory
2. Install Python dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the application:
   ```
   streamlit run app.py
   ```
4. Open your browser to `http://localhost:8501`

## Step 6: Test the Setup

1. Create a new account in the dashboard
2. Try adding some sample water quality data
3. Verify the data appears in the visualization charts

## Troubleshooting

- **Authentication errors**: Check your Supabase URL and API key
- **Database errors**: Ensure the SQL commands ran successfully
- **Import errors**: Make sure all dependencies are installed with `pip install -r requirements.txt`

## Sharing the Dashboard

Once set up, you can share the dashboard by:
1. Deploying to a cloud service (Streamlit Cloud, Heroku, etc.)
2. Sharing the deployed URL with volunteers and stakeholders
3. Only users with accounts can edit data, but all authenticated users can view all data
