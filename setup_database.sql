-- Water Quality Monitoring Database Setup
-- Run these commands in your Supabase SQL Editor

-- Create the water_quality table
CREATE TABLE water_quality (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    site TEXT NOT NULL CHECK (site IN ('Site 1', 'Site 2', 'Site 3')),
    date DATE NOT NULL,
    dissolved_oxygen_mg FLOAT8,
    dissolved_oxygen_sat FLOAT8,
    hardness FLOAT8,
    alkalinity FLOAT8,
    ph FLOAT8,
    temperature FLOAT8,
    flow FLOAT8,
    notes TEXT,
    user_id UUID REFERENCES auth.users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Enable Row Level Security
ALTER TABLE water_quality ENABLE ROW LEVEL SECURITY;

-- Create policy to allow authenticated users to read all data
CREATE POLICY "Allow authenticated users to read all water quality data" ON water_quality
    FOR SELECT USING (auth.role() = 'authenticated');

-- Create policy to allow authenticated users to insert their own data
CREATE POLICY "Allow authenticated users to insert water quality data" ON water_quality
    FOR INSERT WITH CHECK (auth.uid() = user_id);

-- Create policy to allow users to update their own data
CREATE POLICY "Allow users to update their own water quality data" ON water_quality
    FOR UPDATE USING (auth.uid() = user_id);

-- Create policy to allow users to delete their own data
CREATE POLICY "Allow users to delete their own water quality data" ON water_quality
    FOR DELETE USING (auth.uid() = user_id);

-- Create an index for better performance on date queries
CREATE INDEX idx_water_quality_date ON water_quality(date);
CREATE INDEX idx_water_quality_site ON water_quality(site);
CREATE INDEX idx_water_quality_user_id ON water_quality(user_id);
