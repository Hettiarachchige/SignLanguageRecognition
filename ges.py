import cv2  # type: ignore
import numpy as np  # type: ignore
import tensorflow as tf  # type: ignore
import mediapipe as mp  # type: ignore
from PIL import Image, ImageDraw, ImageFont  # type: ignore

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
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

# Load Sinhala font using Pillow
font_path = "NotoSansSinhala-VariableFont_wdth,wght.ttf"
font = ImageFont.truetype(font_path, 40)

# Initialize camera
cap = cv2.VideoCapture(0)
CONFIDENCE_THRESHOLD = 0.7

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break

        # Convert the frame to RGB for MediaPipe processing
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb_frame)

        # Check if hand landmarks are detected
        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                # Draw hand landmarks on the frame
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Extract hand region as input for the model
                h, w, _ = frame.shape
                x_min = int(min([lm.x for lm in hand_landmarks.landmark]) * w)
                y_min = int(min([lm.y for lm in hand_landmarks.landmark]) * h)
                x_max = int(max([lm.x for lm in hand_landmarks.landmark]) * w)
                y_max = int(max([lm.y for lm in hand_landmarks.landmark]) * h)

                # Crop the hand region from the frame
                hand_region = frame[y_min:y_max, x_min:x_max]
                if hand_region.size > 0:
                    # Preprocess the hand region for the model
                    hand_resized = cv2.resize(hand_region, (64, 64))
                    hand_normalized = np.expand_dims(hand_resized / 255.0, axis=0)

                    # Get predictions from the model
                    predictions = model.predict(hand_normalized)
                    if predictions.size == 0:
                        print("No predictions returened.")
                    
                    else:
                         predicted_class = np.argmax(predictions[0])
                    if predicted_class < len(class_names):
                       confidence = predictions[0][predicted_class]

                    # Only display gesture name if confidence exceeds the threshold
                    sinhala_text = sinhala_mapping.get(class_names[predicted_class], '') if confidence >= CONFIDENCE_THRESHOLD else ''
                    if confidence >= CONFIDENCE_THRESHOLD:
                    # Only render text if there are detected landmarks
                     if sinhala_text:
                        # Render Sinhala text using Pillow
                        pil_img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                        draw = ImageDraw.Draw(pil_img)
                        draw.text((50, 50), sinhala_text, font=font, fill=(0, 255, 0))

                        # Convert back to OpenCV format
                        frame = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

        # Show the frame
        cv2.imshow('Sign Language Recognition', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
except Exception as e:
    print("Error:", e)
finally:
    cap.release()
    cv2.destroyAllWindows()
