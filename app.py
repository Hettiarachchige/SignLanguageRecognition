# app.py
import base64
from flask import Flask, request, jsonify
import cv2  # type: ignore
import numpy as np  # type: ignore
import tensorflow as tf  # type: ignore
import mediapipe as mp  # type: ignore
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Load the gesture model
model = tf.keras.models.load_model('gesture_model.keras')

# Class names and Sinhala text mappings
class_names = ['hello', 'one', 'welcome']
sinhala_mapping = {
    'hello': 'ආයුබෝවන්',
    'one': 'එක',
    'welcome': 'සාදරයෙන් පිළිගනිමු'
}

# MediaPipe setup for hand detection
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.2)

@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
    return response

@app.route('/api/recognize', methods=['POST'])
def predict():
    # Get image data from request body (assuming JSON format)
    data = request.get_json()
    image_data = data.get('image')

    if not image_data:
      print("not json")
      return jsonify({'error': 'Missing image data'}), 400

    decoded_data = base64.b64decode(image_data)

    np_img = np.frombuffer(decoded_data, np.uint8)

    frame = cv2.imdecode(np_img, cv2.IMREAD_COLOR)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    result = hands.process(rgb_frame)
    # print(f"Hand landmarks: {result.multi_hand_landmarks}")  # Log the result
    
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            # Extract hand region
            h, w, _ = frame.shape
            x_min = int(min([lm.x for lm in hand_landmarks.landmark]) * w)
            y_min = int(min([lm.y for lm in hand_landmarks.landmark]) * h)
            x_max = int(max([lm.x for lm in hand_landmarks.landmark]) * w)
            y_max = int(max([lm.y for lm in hand_landmarks.landmark]) * h)

            hand_region = frame[y_min:y_max, x_min:x_max]
            if hand_region.size > 0:
                hand_resized = cv2.resize(hand_region, (64, 64))
                hand_normalized = np.expand_dims(hand_resized / 255.0, axis=0)

                predictions = model.predict(hand_normalized)
                predicted_class = np.argmax(predictions[0])
                confidence = predictions[0][predicted_class]

                if confidence >= 0.5:
                    gesture = class_names[predicted_class]
                    sinhala_text = sinhala_mapping.get(gesture, '')
                    
                    print("gesture: " + gesture)

                    # Add CORS headers for any origin
                    response = jsonify({'gesture': gesture, 'sinhala': sinhala_text})
                    response.headers['Access-Control-Allow-Origin'] = '*'

                    return response

    return jsonify({'error': 'No valid gesture detected'}), 400

if __name__ == '__main__':
    app.run(debug=True)
