# app/app.py
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import tensorflow as tf
from PIL import Image
import numpy as np
import os
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///diagnosis_database.db'  # SQLite database file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Model for storing diagnosis records
class Diagnosis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    diagnosis_result = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

db.create_all()  # Create tables in the database

model = tf.keras.models.load_model('../model/your_pretrained_model.h5')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/diagnose', methods=['POST'])
def diagnose():
    try:
        file = request.files['image']
        img = Image.open(file.stream).convert("RGB")
        img = img.resize((224, 224))
        img_array = np.array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        predictions = model.predict(img_array)
        diagnosis_result = process_predictions(predictions)

        # Save diagnosis result to the database
        save_diagnosis_result(diagnosis_result)

        return jsonify({'diagnosis': diagnosis_result})

    except Exception as e:
        return jsonify({'error': str(e)})

def process_predictions(predictions):
    # Implement logic to interpret model predictions
    # For simplicity, return 'Normal' or 'Abnormal' based on a threshold
    return 'Normal' if predictions[0][0] > 0.5 else 'Abnormal'

def save_diagnosis_result(diagnosis_result):
    # Save diagnosis result to the database
    new_diagnosis = Diagnosis(diagnosis_result=diagnosis_result)
    db.session.add(new_diagnosis)
    db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)

