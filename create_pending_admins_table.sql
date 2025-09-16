-- Create pending_admins table for admin approval workflow
CREATE TABLE IF NOT EXISTS pending_admins (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    requested_at TIMESTAMP DEFAULT NOW(),
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'approved', 'denied')),
    approved_by VARCHAR(255),
    approved_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create index for faster queries
CREATE INDEX IF NOT EXISTS idx_pending_admins_email ON pending_admins(email);
CREATE INDEX IF NOT EXISTS idx_pending_admins_status ON pending_admins(status);
