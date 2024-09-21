import sqlite3

# Connect to the database (it will be created if it doesn't exist)
conn = sqlite3.connect('jobs.db')

# Create a cursor object
cursor = conn.cursor()

# Create the candidates table
cursor.execute('''
CREATE TABLE IF NOT EXISTS candidates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    mobile TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    current_company TEXT,
    designation TEXT,
    work_experience TEXT,
    total_experience INTEGER,
    address TEXT,
    location TEXT NOT NULL
);
''')

# Create the dealers table
cursor.execute('''
CREATE TABLE IF NOT EXISTS dealers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dealership_name TEXT NOT NULL,
    location TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    contact_number TEXT NOT NULL,
    subscription_plan TEXT
);
''')

# Create the jobs table
cursor.execute('''
CREATE TABLE IF NOT EXISTS jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dealer_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    department TEXT NOT NULL,
    location TEXT NOT NULL,
    experience_level TEXT,
    FOREIGN KEY (dealer_id) REFERENCES dealers (id)
);
''')

# Create the admin table
cursor.execute('''
CREATE TABLE IF NOT EXISTS admin (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    admin_id TEXT NOT NULL,
    password TEXT NOT NULL
);
''')

# Commit changes and close the connection
conn.commit()
conn.close()

print("Database and tables created successfully.")
