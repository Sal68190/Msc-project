# app/app.py
from flask import Flask, render_template, request, jsonify
import tensorflow as tf
from PIL import Image
import numpy as np

app = Flask(__name__)

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

        return jsonify({'diagnosis': diagnosis_result})

    except Exception as e:
        return jsonify({'error': str(e)})

def process_predictions(predictions):
    # Implement logic to interpret model predictions
    # For simplicity, return 'Normal' or 'Abnormal' based on a threshold
    return 'Normal' if predictions[0][0] > 0.5 else 'Abnormal'

if __name__ == '__main__':
    app.run(debug=True)
