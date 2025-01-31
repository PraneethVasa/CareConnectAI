from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from datetime import datetime
import joblib
import google.generativeai as genai

app = Flask(__name__)
app.secret_key = 'careconnect_secret_key'

# Gemini API configuration
genai.configure(api_key='AIzaSyAh78MT0xRVUPqg7NouDTBV_8YBtJ1BGdc')
model = genai.GenerativeModel('gemini-pro')

# Load trained model
disease_model = joblib.load('models/disease_model.joblib')

# Database connection
def get_db_connection():
    conn = sqlite3.connect('database/careconnect.db')
    conn.row_factory = sqlite3.Row
    return conn

# Home route
@app.route('/')
def home():
    return render_template('login.html')

# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        mobile = request.form['mobile']
        email = request.form['email']
        password = request.form['password']
        security_question = request.form['security_question']
        security_answer = request.form['security_answer']
        language = request.form['language']
        username = f"user_{mobile}"  # Generate unique username

        conn = get_db_connection()
        conn.execute('INSERT INTO users (username, name, mobile, email, password, security_question, security_answer, language) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                     (username, name, mobile, email, password, security_question, security_answer, language))
        conn.commit()
        conn.close()

        flash('Registration successful! Please login.')
        return redirect(url_for('login'))
    return render_template('register.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password)).fetchone()
        conn.close()

        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['language'] = user['language']
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.')
    return render_template('login.html')

# Dashboard route
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    # Greet user
    greeting = f"Hello, {session['username']}! Welcome to CareConnect AI."
    return render_template('dashboard.html', greeting=greeting)

# Symptom analysis route
@app.route('/symptom_check', methods=['GET', 'POST'])
def symptom_check():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        age = int(request.form['age'])
        gender = request.form['gender']
        symptoms = request.form['symptoms']

        # Predict disease
        prediction = disease_model.predict([[age, gender, symptoms]])[0]
        precautions = model.generate_content(f"Give precautions for {prediction}").text

        return render_template('symptom_check.html', prediction=prediction, precautions=precautions)
    return render_template('symptom_check.html')

# Doctor consultation route
@app.route('/doctor_consult')
def doctor_consult():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    doctors = conn.execute('SELECT * FROM doctors').fetchall()
    conn.close()

    return render_template('doctor_consult.html', doctors=doctors)

# Forgot password route
@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        username = request.form['username']
        security_answer = request.form['security_answer']

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ? AND security_answer = ?', (username, security_answer)).fetchone()
        conn.close()

        if user:
            flash(f"Your password is: {user['password']}")
        else:
            flash('Invalid username or security answer.')
    return render_template('forgot_password.html')

# Logout route
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
