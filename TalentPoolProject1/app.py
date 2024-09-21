from flask import Flask, request, render_template, redirect, url_for, session, flash
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'namishamitrubyusha110920130510198215011982310316202112006your_secret_key'

def connect_db():
    return sqlite3.connect('jobs.db')

# Home page
@app.route('/')
def home():
    return render_template('index.html')

# Candidate registration
@app.route('/register_candidate', methods=['POST', 'GET'])
def register_candidate():
    if request.method == 'POST':
        conn = connect_db()
        cursor = conn.cursor()
        password_hash = generate_password_hash(request.form['password'])
        cursor.execute('''INSERT INTO candidates (name, mobile, email, password, current_company, designation, work_experience, total_experience, address, location)
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                        (request.form['name'], request.form['mobile'], request.form['email'], password_hash,
                         request.form['current_company'], request.form['designation'], request.form['work_experience'],
                         request.form['total_experience'], request.form['address'], request.form['location']))
        conn.commit()
        conn.close()
        return redirect(url_for('login_candidate'))
    return render_template('register_candidate.html')

# Candidate login
@app.route('/login_candidate', methods=['POST', 'GET'])
def login_candidate():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM candidates WHERE email = ?', (email,))
        candidate = cursor.fetchone()
        conn.close()
        if candidate and check_password_hash(candidate[4], password):
            session['candidate_id'] = candidate[0]
            return redirect(url_for('view_job_openings'))
        flash('Invalid credentials')
    return render_template('login_candidate.html')

# View job openings for candidates
@app.route('/view_job_openings')
def view_job_openings():
    if 'candidate_id' in session:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM jobs')
        jobs = cursor.fetchall()
        conn.close()
        return render_template('job_listings.html', jobs=jobs)
    return redirect(url_for('login_candidate'))

# Dealer registration
@app.route('/register_dealer', methods=['POST', 'GET'])
def register_dealer():
    if request.method == 'POST':
        conn = connect_db()
        cursor = conn.cursor()
        password_hash = generate_password_hash(request.form['password'])
        cursor.execute('''INSERT INTO dealers (dealership_name, location, email, password, contact_number, subscription_plan)
                          VALUES (?, ?, ?, ?, ?, ?)''',
                        (request.form['dealership_name'], request.form['location'], request.form['email'], password_hash,
                         request.form['contact_number'], request.form['subscription_plan']))
        conn.commit()
        conn.close()
        return redirect(url_for('login_dealer'))
    return render_template('register_dealer.html')

# Dealer login
@app.route('/login_dealer', methods=['POST', 'GET'])
def login_dealer():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM dealers WHERE email = ?', (email,))
        dealer = cursor.fetchone()
        conn.close()
        if dealer and check_password_hash(dealer[4], password):
            session['dealer_id'] = dealer[0]
            return redirect(url_for('post_job'))
        flash('Invalid credentials')
    return render_template('login_dealer.html')

# Post job by dealer
@app.route('/post_job', methods=['POST', 'GET'])
def post_job():
    if 'dealer_id' in session:
        if request.method == 'POST':
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO jobs (dealer_id, title, department, location, experience_level)
                              VALUES (?, ?, ?, ?, ?)''',
                            (session['dealer_id'], request.form['title'], request.form['department'],
                             request.form['location'], request.form['experience_level']))
            conn.commit()
            conn.close()
            flash('Job posted successfully')
            return redirect(url_for('post_job'))
        return render_template('post_job.html')
    return redirect(url_for('login_dealer'))

# Admin login
@app.route('/admin_login', methods=['POST', 'GET'])
def admin_login():
    if request.method == 'POST':
        if request.form['admin_id'] == 'Amit1982' and request.form['password'] == 'Namish1982':
            session['admin_logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        flash('Invalid admin credentials')
    return render_template('admin_login.html')

# Admin dashboard
@app.route('/admin_dashboard')
def admin_dashboard():
    if 'admin_logged_in' in session:
        return render_template('admin_dashboard.html')
    return redirect(url_for('admin_login'))

# Admin - Manage jobs
@app.route('/manage_jobs')
def manage_jobs():
    if 'admin_logged_in' in session:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM jobs')
        jobs = cursor.fetchall()
        conn.close()
        return render_template('manage_jobs.html', jobs=jobs)
    return redirect(url_for('admin_login'))

# Add job opportunity (Admin only)
@app.route('/add_job', methods=['POST', 'GET'])
def add_job():
    if 'admin_logged_in' in session:
        if request.method == 'POST':
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO jobs (dealer_id, title, department, location, experience_level)
                              VALUES (?, ?, ?, ?, ?)''',
                            (request.form['dealer_id'], request.form['title'], request.form['department'],
                             request.form['location'], request.form['experience_level']))
            conn.commit()
            conn.close()
            return redirect(url_for('manage_jobs'))
        return render_template('add_job.html')
    return redirect(url_for('admin_login'))

# Remove job opportunity (Admin only)
@app.route('/remove_job/<int:job_id>', methods=['POST'])
def remove_job(job_id):
    if 'admin_logged_in' in session:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM jobs WHERE id = ?', (job_id,))
        conn.commit()
        conn.close()
        return redirect(url_for('manage_jobs'))
    return redirect(url_for('admin_login'))

# Admin - Manage users
@app.route('/manage_users')
def manage_users():
    if 'admin_logged_in' in session:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM candidates')
        candidates = cursor.fetchall()
        cursor.execute('SELECT * FROM dealers')
        dealers = cursor.fetchall()
        conn.close()
        return render_template('manage_users.html', candidates=candidates, dealers=dealers)
    return redirect(url_for('admin_login'))

# Forgot password
@app.route('/forgot_password', methods=['POST', 'GET'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        # Simulate password reset logic
        flash('Password reset link sent to ' + email)
    return render_template('forgot_password.html')

# Terms & Conditions
@app.route('/terms_conditions')
def terms_conditions():
    return render_template('terms_conditions.html')

# Contact Us
@app.route('/contact_us')
def contact_us():
    return render_template('contact_us.html')

# Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
