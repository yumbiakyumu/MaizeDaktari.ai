from flask import Flask, request, render_template, redirect, session, jsonify
import sqlite3
import os
from contextlib import contextmanager
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.secret_key = os.urandom(32)

# Connect to the SQLite database
conn = sqlite3.connect('users.db', check_same_thread=False)

@contextmanager
def get_db():
    db = conn
    cursor = db.cursor()
    try:
        yield cursor
    finally:
        cursor.close()

# Create a table 
with get_db() as c:
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, email TEXT, password TEXT, is_admin INTEGER DEFAULT 0)''')
    conn.commit()

# Registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        with get_db() as c:
            # Check if the username or email already exists
            c.execute("SELECT * FROM users WHERE username = ? OR email = ?", (username, email))
            existing_user = c.fetchone()

            if existing_user:
                return jsonify({'message': 'Username or email already exists'})

            # Insert the new user into the database
            c.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", (username, email, hashed_password))
            conn.commit()

        return jsonify({'redirect': '/login', 'message': 'User successfully registered'})

    return render_template('register.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        with get_db() as c:
            # Check if the username exists
            c.execute("SELECT * FROM users WHERE username = ?", (username,))
            user = c.fetchone()

            if user and check_password_hash(user[3], password):
                session['username'] = username  
                session['is_admin'] = user[4]  

                if session['is_admin']:
                    return jsonify({'redirect': '/dashboard', 'message': 'Logged in as admin'})
                else:
                    return jsonify({'redirect': '/', 'message': 'Logged in successfully'})
            else:
                return jsonify({'message': 'Invalid username or password'})

    return render_template('login.html')
# Logout route
@app.route('/logout')
def logout():
    session.pop('username', None)  
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)