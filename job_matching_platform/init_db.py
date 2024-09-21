# init_db.py
import sqlite3

def init_db():
    conn = sqlite3.connect('jobs.db')
    cursor = conn.cursor()

    # Create tables
    cursor.execute('''CREATE TABLE IF NOT EXISTS candidates (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        mobile TEXT NOT NULL,
                        email TEXT NOT NULL,
                        current_company TEXT,
                        designation TEXT,
                        work_experience TEXT,
                        total_experience INTEGER,
                        address TEXT,
                        location TEXT
                    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS dealers (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        dealership_name TEXT NOT NULL,
                        location TEXT NOT NULL,
                        contact_email TEXT NOT NULL,
                        contact_number TEXT NOT NULL,
                        subscription_plan TEXT NOT NULL
                    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS jobs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        dealer_id INTEGER,
                        title TEXT NOT NULL,
                        department TEXT NOT NULL,
                        location TEXT NOT NULL,
                        experience_level TEXT NOT NULL,
                        FOREIGN KEY (dealer_id) REFERENCES dealers(id)
                    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS applications (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        candidate_id INTEGER,
                        job_id INTEGER,
                        status TEXT NOT NULL,
                        FOREIGN KEY (candidate_id) REFERENCES candidates(id),
                        FOREIGN KEY (job_id) REFERENCES jobs(id)
                    )''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
