from flask import Flask, request, render_template, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management and flash messages

def connect_db():
    return sqlite3.connect('jobs.db')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register_candidate', methods=['GET', 'POST'])
def register_candidate():
    if request.method == 'POST':
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO candidates (name, mobile, email, current_company, designation, work_experience, total_experience, address, location)
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                      (request.form['name'], request.form['mobile'], request.form['email'], request.form['current_company'],
                       request.form['designation'], request.form['work_experience'], request.form['total_experience'],
                       request.form['address'], request.form['location']))
        conn.commit()
        conn.close()
        flash('Candidate registered successfully!')
        return redirect(url_for('home'))
    return render_template('register_candidate.html')

@app.route('/register_dealer', methods=['GET', 'POST'])
def register_dealer():
    if request.method == 'POST':
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO dealers (dealership_name, location, contact_email, contact_number, subscription_plan)
                          VALUES (?, ?, ?, ?, ?)''',
                      (request.form['dealership_name'], request.form['location'], request.form['contact_email'],
                       request.form['contact_number'], request.form['subscription_plan']))
        conn.commit()
        conn.close()
        flash('Dealer registered successfully!')
        return redirect(url_for('home'))
    return render_template('register_dealer.html')

@app.route('/post_job', methods=['GET', 'POST'])
def post_job():
    if request.method == 'POST':
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO jobs (dealer_id, title, department, location, experience_level)
                          VALUES (?, ?, ?, ?, ?)''',
                      (request.form['dealer_id'], request.form['title'], request.form['department'],
                       request.form['location'], request.form['experience_level']))
        conn.commit()
        conn.close()
        flash('Job posted successfully!')
        return redirect(url_for('home'))
    return render_template('post_job.html')

@app.route('/job_listings')
def job_listings():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''SELECT jobs.id, jobs.title, jobs.department, jobs.location, jobs.experience_level, dealers.dealership_name
                      FROM jobs
                      JOIN dealers ON jobs.dealer_id = dealers.id''')
    jobs = cursor.fetchall()
    conn.close()
    return render_template('job_listings.html', jobs=jobs)

@app.route('/sign_up_candidate', methods=['GET', 'POST'])
def sign_up_candidate():
    if request.method == 'POST':
        # Implement sign-up logic here (e.g., save user details)
        pass
    return render_template('sign_up_candidate.html')

@app.route('/forgot_password_candidate', methods=['GET', 'POST'])
def forgot_password_candidate():
    if request.method == 'POST':
        # Implement forgot password logic here (e.g., send reset link)
        pass
    return render_template('forgot_password_candidate.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        if request.form['admin_id'] == 'Amit1982' and request.form['password'] == 'Namish1982':
            return redirect(url_for('home'))
        else:
            flash('Invalid credentials', 'error')
    return render_template('admin_login.html')

if __name__ == '__main__':
    app.run(debug=True)
