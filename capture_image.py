import cv2  # type: ignore
import mediapipe as mp  # type: ignore
import os
import time

# Define paths and parameters
GESTURE_NAME = input("Enter gesture name: ")
SAVE_PATH = f"gestures/{GESTURE_NAME}"
os.makedirs(SAVE_PATH, exist_ok=True)

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

# Set the number of images to capture
TOTAL_IMAGES = 1000
count = 0

print(f"Capturing {TOTAL_IMAGES} images for gesture '{GESTURE_NAME}'. Press 'q' to quit at any time.")

while count < TOTAL_IMAGES:
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture image.")
        break

    # Convert the frame to RGB for MediaPipe processing
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = holistic.process(frame_rgb)

    # Draw landmarks on the frame
    if results.pose_landmarks:
        mp_drawing.draw_landmarks(
            frame, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS
        )
    #if results.face_landmarks:
       # mp_drawing.draw_landmarks(
       #     frame, results.face_landmarks, mp_holistic.FACEMESH_TESSELATION
        #)
    if results.left_hand_landmarks:
        mp_drawing.draw_landmarks(
            frame, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS
        )
    if results.right_hand_landmarks:
        mp_drawing.draw_landmarks(
            frame, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS
        )

    # Show the frame with landmarks
    cv2.imshow("Capture Gesture with Holistic Landmarks", frame)

    # Save the image if any landmarks are detected
    if (
        results.pose_landmarks
        #or results.face_landmarks
        or results.left_hand_landmarks
        or results.right_hand_landmarks
    ):
        img_name = f"{SAVE_PATH}/{GESTURE_NAME}_{count}.jpg"
        cv2.imwrite(img_name, frame)
        print(f"Saved: {img_name}")
        count += 1

    # Wait a moment before capturing the next image
    time.sleep(0.1)  # Adjust this to control capture speed

    # Exit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
print(f"Captured {count} images for gesture '{GESTURE_NAME}'.")
