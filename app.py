from flask import Flask, request, jsonify, render_template, url_for, session, redirect, send_from_directory
from flask_cors import CORS
import tensorflow as tf
import numpy as np
from PIL import Image
import io
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import layers
import os
import sqlite3
from datetime import datetime

# Import the register and login functions from auth.py
from auth import register, login

# Load the pre-trained model
model = tf.keras.models.load_model('maize_model2.h5')
class_names = ['blight', 'common_rust', 'gray_leaf_spot', 'healthy']

app = Flask(__name__, static_url_path='/static')
app.secret_key = os.urandom(32)
CORS(app)

# Register routes from auth.py
app.add_url_rule('/register', view_func=register, methods=['GET', 'POST'])
app.add_url_rule('/login', view_func=login, methods=['GET', 'POST'])

# Data augmentation for training (optional)
datagen = ImageDataGenerator(
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest'
)

# Preprocessing function
def preprocess_image(image):
    resize_and_rescale = tf.keras.Sequential([
        layers.Resizing(256, 256), 
        layers.Rescaling(1.0 / 255)
    ])
    image = resize_and_rescale(image)
    # data_augmentation = tf.keras.Sequential([
    #     layers.experimental.preprocessing.RandomFlip("horizontal_and_vertical"),
    #     layers.experimental.preprocessing.RandomRotation(0.3),
    # ])
    # image = data_augmentation(image)
    image = np.expand_dims(image, axis=0)
    return image

def save_diagnosis_record(username, image_path, prediction, control_info):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO diagnosis_records (username, image_path, prediction, control_info, timestamp)
    VALUES (?, ?, ?, ?, ?)
    ''', (username, image_path, prediction, control_info, datetime.now()))
    conn.commit()
    conn.close()

def get_user_details(username):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT username, email FROM users WHERE username = ?', (username,))
    user_details = cursor.fetchone()
    conn.close()
    return user_details

def get_diagnosis_records(username):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
    SELECT image_path, prediction, control_info, timestamp
    FROM diagnosis_records
    WHERE username = ?
    ORDER BY timestamp DESC
    ''', (username,))
    records = cursor.fetchall()
    conn.close()
    return records

def save_query(username, subject, message):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO queries (username, subject, message, timestamp)
    VALUES (?, ?, ?, ?)
    ''', (username, subject, message, datetime.now()))
    conn.commit()
    conn.close()

def get_queries():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, username, subject, message, timestamp FROM queries ORDER BY timestamp DESC')
    queries = cursor.fetchall()
    conn.close()
    return queries

@app.route('/')
def index():
    image_url = url_for('static', filename='images/pexel 2.jpeg')
    return render_template('index.html', hero_bg_image=image_url)

@app.route('/predict', methods=['POST'])
def predict():
    if 'username' in session:
        username = session['username']
    else:
        username = None

    file = request.files['image']
    img = Image.open(io.BytesIO(file.read()))
    img_array = img_to_array(img)
    preprocessed_image = preprocess_image(img_array)
    prediction = model.predict(preprocessed_image)

    print("Preprocessed image shape:", preprocessed_image.shape)

    prediction = model.predict(preprocessed_image)
    print("Prediction raw output:", prediction)

    predicted_class_index = np.argmax(prediction[0])
    predicted_class = class_names[predicted_class_index]

    print("Predicted class index:", predicted_class_index)
    print("Predicted class:", predicted_class)

    if predicted_class == 'blight':
        control_info = "Use recommended fungicides early, especially in wet conditions. Rotate crops to prevent pathogen buildup. Remove and destroy infected plants promptly. Enhance air circulation by proper spacing and pruning. Avoid overhead watering to minimize leaf wetness."
    elif predicted_class == 'common_rust':
        control_info = "Plant rust-resistant crop varieties. Apply fungicides as recommended. Regularly inspect plants for early signs of rust. Rotate with non-host crops. Eliminate volunteer plants that can harbor pathogens."
    elif predicted_class == 'gray_leaf_spot':
        control_info = "Apply appropriate fungicides early. Rotate crops to reduce soil-borne pathogens. Plant resistant varieties. Ensure proper spacing for better air circulation. Remove and destroy crop residues after harvest."
    else:
        control_info = "Your plant appears to be healthy."

    img_filename = file.filename
    img_path = os.path.join('static/uploads', img_filename)
    img.save(img_path)
    img_url = url_for('static', filename=f'uploads/{img_filename}')

    save_diagnosis_record(username, img_path, predicted_class, control_info)

    response = {
        'prediction': predicted_class,
        'control_info': control_info,
        'image_url': img_url
    }

    return jsonify(response)

@app.route('/results', methods=['GET'])
def results():
    prediction = request.args.get('prediction', '')
    control_info = request.args.get('control_info', '')
    image_url = request.args.get('image_url', '')
    return render_template('results.html', prediction=prediction, control_info=control_info, image_url=image_url)

@app.route('/dashboard')
def dashboard():
    if 'username' in session and session['is_admin']:
        return render_template('dashboard.html')
    else:
        return redirect('/login')

@app.route('/userdashboard')
def userdashboard():
    if 'username' not in session:
        return redirect('/login')

    username = session['username']
    user_details = get_user_details(username)
    diagnosis_records = get_diagnosis_records(username)

    print(f"User Details: {user_details}")
    print(f"Diagnosis Records: {diagnosis_records}")

    return render_template('userdashboard.html', user_details=user_details, diagnosis_records=diagnosis_records)

@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM users WHERE username = ? OR email = ?", (username, email))
    existing_user = cursor.fetchone()
    if existing_user:
        return jsonify({'message': 'Username or email already exists'}), 400
    
    cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", (username, email, password))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'User added successfully'})

@app.route('/remove_user', methods=['POST'])
def remove_user():
    data = request.json
    username = data.get('username')
    
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM users WHERE username = ?", (username,))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'User removed successfully'})

@app.route('/get_users')
def get_users():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, username, email FROM users")
    users = cursor.fetchall()
    conn.close()
    
    return jsonify([{'id': user[0], 'username': user[1], 'email': user[2]} for user in users])

@app.route('/get_admin_profile')
def get_admin_profile():
    if 'username' in session and session['is_admin']:
        username = session['username']
        
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        
        cursor.execute("SELECT username, email FROM users WHERE username = ?", (username,))
        admin_profile = cursor.fetchone()
        conn.close()
        
        if admin_profile:
            return jsonify({'username': admin_profile[0], 'email': admin_profile[1]})
        else:
            return jsonify({'message': 'Admin not found'}), 404
    else:
        return jsonify({'message': 'Unauthorized'}), 401

@app.route('/submit_query', methods=['POST'])
def submit_query():
    if 'username' in session:
        username = session['username']
        data = request.json
        subject = data.get('subject')
        message = data.get('message')
        save_query(username, subject, message)
        return jsonify({'message': 'Query submitted successfully'})
    else:
        return jsonify({'message': 'Please log in to submit a query'}), 401

@app.route('/queries')
def queries():
    if 'username' in session and session['is_admin']:
        queries = get_queries()
        return jsonify(queries)
    else:
        return jsonify({'message': 'Unauthorized access'}), 403

@app.route('/get_analytics')
def get_analytics():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    
    cursor.execute("SELECT COUNT(*) FROM diagnosis_records WHERE timestamp >= datetime('now', 'start of month')")
    user_activity = cursor.fetchone()[0]
    
    
    
    conn.close()
    
    return jsonify({
        'user_activity': user_activity,
        'page_views': 340230,
        'emails_received': 47500,
        'diseases_diagnosed': 2500,
        'images_uploaded': 10000
    })





@app.route('/add_task', methods=['POST'])
def add_task():
    data = request.json
    task = data.get('task')
    date = data.get('date')
    
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO tasks (description, date, completed) VALUES (?, ?, ?)", (task, date, 0))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Task added successfully'})

@app.route('/get_tasks')
def get_tasks():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, description, date, completed FROM tasks WHERE completed = 0")
    tasks = cursor.fetchall()
    conn.close()
    
    return jsonify([{'id': task[0], 'description': task[1], 'date': task[2], 'completed': task[3]} for task in tasks])

@app.route('/complete_task/<int:task_id>', methods=['POST'])
def complete_task(task_id):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    cursor.execute("UPDATE tasks SET completed = 1 WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Task completed successfully'})

@app.route('/logout')
def logout():
    
    session.clear()
    return redirect(url_for('index'))
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)