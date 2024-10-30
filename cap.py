import os
import numpy as np
import cv2
import mediapipe as mp
import time

# Define paths and parameters
GESTURE_NAME = input("Enter gesture name: ")
SAVE_PATH = f"gestures/{GESTURE_NAME}"
os.makedirs(SAVE_PATH, exist_ok=True)

# Actions to detect
actions = np.array(['hello', 'thanks', 'iloveyou'])

# Parameters for video capturing
no_sequences = 30
sequence_length = 30
start_folder = 30

# Initialize MediaPipe Holistic and camera
mp_holistic = mp.solutions.holistic
mp_drawing = mp.solutions.drawing_utils

holistic = mp_holistic.Holistic(
    static_image_mode=False,
    model_complexity=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5,
)

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Camera not detected.")
    exit()

# Create directories for each action and initialize directories
for action in actions:
    action_dir = os.path.join(SAVE_PATH, action)
    os.makedirs(action_dir, exist_ok=True)
    dirmax = np.max(np.array(os.listdir(action_dir)).astype(int), initial=0)
    for sequence in range(1, no_sequences + 1):
        os.makedirs(os.path.join(action_dir, str(dirmax + sequence)), exist_ok=True)

def mediapipe_detection(image, model):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image.flags.writeable = False  # False allows for faster processing
    results = model.process(image)
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    return image, results

def extract_keypoints(results):
    keypoints = []
    if results.pose_landmarks:
        for landmark in results.pose_landmarks.landmark:
            keypoints.append([landmark.x, landmark.y, landmark.z])
    return np.array(keypoints).flatten()

print(f"Capturing images for gesture '{GESTURE_NAME}'. Press 'q' to quit at any time.")

# Capture images and keypoints for each action
for action in actions:
    for sequence in range(start_folder, start_folder + no_sequences):
        for frame_num in range(sequence_length):
            ret, frame = cap.read()
            if not ret:
                print("Failed to capture image.")
                break

            # Make detections
            image, results = mediapipe_detection(frame, holistic)

            # Draw landmarks
            if results.pose_landmarks:
                mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS)
            if results.face_landmarks:
                mp_drawing.draw_landmarks(image, results.face_landmarks, mp_holistic.FACEMESH_TESSELATION)
            if results.left_hand_landmarks:
                mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
            if results.right_hand_landmarks:
                mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS)

            # Show the frame with landmarks
            cv2.imshow("Capture Gesture with Holistic Landmarks", image)

            # Export keypoints
            keypoints = extract_keypoints(results)
            npy_path = os.path.join(SAVE_PATH, action, str(sequence), str(frame_num))
            np.save(npy_path, keypoints)

            if frame_num == 0:
                cv2.putText(image, 'STARTING COLLECTION', (120, 200),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 4, cv2.LINE_AA)
                cv2.putText(image, 'Collecting frames for {} Video Number {}'.format(action, sequence), (15, 12),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
                cv2.imshow('OpenCV Feed', image)
                cv2.waitKey(500)
            else:
                cv2.putText(image, 'Collecting frames for {} Video Number {}'.format(action, sequence), (15, 12),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
                cv2.imshow('OpenCV Feed', image)

            # Break gracefully if 'q' is pressed
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break
            
            # Wait a moment before capturing the next image
            time.sleep(0.1)

cap.release()
cv2.destroyAllWindows()
print(f"Finished capturing images for gesture '{GESTURE_NAME}'.")
