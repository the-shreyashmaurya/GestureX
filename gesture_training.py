import numpy as np
import tensorflow as tf
import cv2
import mediapipe as mp
import os
import json
from gesture_recognition import GestureRecognition
from gesture_control import add_custom_command, execute_command

# Initialize MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

# Gesture data storage
DATASET_PATH = "dataset/gesture_data.json"
MODEL_PATH = "model/gesture_model.h5"

# Ensure dataset directory exists
os.makedirs("dataset", exist_ok=True)

# Load existing gestures if available
if os.path.exists(DATASET_PATH):
    with open(DATASET_PATH, "r") as f:
        data = json.load(f)
        GESTURE_CLASSES = data.get("classes", {})
        GESTURE_DATA = data.get("data", [])
else:
    GESTURE_CLASSES = {}
    GESTURE_DATA = []


def collect_gesture_data(label_name):
    """Collects hand landmarks for the given label (gesture)."""
    global GESTURE_CLASSES, GESTURE_DATA
    
    cap = cv2.VideoCapture(0)
    collected_samples = 0
    label_id = GESTURE_CLASSES.get(label_name, len(GESTURE_CLASSES))

    if label_name not in GESTURE_CLASSES:
        GESTURE_CLASSES[label_name] = label_id

    print(f"Collecting data for gesture: {label_name} (ID: {label_id})")
    
    while collected_samples < 1000:  # Collect 100 samples per gesture
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb_frame)

        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                landmarks = np.array([[lm.x, lm.y, lm.z] for lm in hand_landmarks.landmark]).flatten()
                GESTURE_DATA.append({"label": label_id, "landmarks": landmarks.tolist()})
                collected_samples += 1

        cv2.putText(frame, f"Collecting {label_name}: {collected_samples}/1000", (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.imshow("Gesture Collection", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    # Save dataset
    with open(DATASET_PATH, "w") as f:
        json.dump({"classes": GESTURE_CLASSES, "data": GESTURE_DATA}, f)

    print(f"Gesture data saved for: {label_name}")


def delete_gesture_data(label_name):
    """Deletes gesture data for a specific label."""
    global GESTURE_CLASSES, GESTURE_DATA
    
    if label_name in GESTURE_CLASSES:
        label_id = GESTURE_CLASSES[label_name]
        GESTURE_DATA = [entry for entry in GESTURE_DATA if entry["label"] != label_id]
        del GESTURE_CLASSES[label_name]
        
        with open(DATASET_PATH, "w") as f:
            json.dump({"classes": GESTURE_CLASSES, "data": GESTURE_DATA}, f)
        
        print(f"Gesture data deleted for: {label_name}")
    else:
        print(f"Gesture '{label_name}' not found in dataset.")


def delete_all_trained_data():
    """Deletes all trained gesture data and resets the model."""
    global GESTURE_CLASSES, GESTURE_DATA
    
    if os.path.exists(DATASET_PATH):
        os.remove(DATASET_PATH)
    if os.path.exists(MODEL_PATH):
        os.remove(MODEL_PATH)
    
    GESTURE_CLASSES = {}
    GESTURE_DATA = []
    
    print("All trained gesture data and model have been deleted.")


def train_model():
    """Trains the deep learning model with collected gesture data."""
    if len(GESTURE_DATA) == 0:
        print("No gesture data found. Collect data before training.")
        return

    X = np.array([entry["landmarks"] for entry in GESTURE_DATA])
    y = np.array([entry["label"] for entry in GESTURE_DATA])

    y_one_hot = tf.keras.utils.to_categorical(y, num_classes=len(GESTURE_CLASSES))

    model = GestureRecognition()._create_model(len(GESTURE_CLASSES))
    model.fit(X, y_one_hot, epochs=20, batch_size=16)

    model.save(MODEL_PATH)
    print("Model training complete and saved.")


if __name__ == "__main__":
    while True:
        print("\n1. Collect Gesture Data")
        print("2. Train Model")
        print("3. Delete Gesture Data")
        print("4. Delete All Trained Data")
        print("5. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            gesture_name = input("Enter gesture name: ")
            collect_gesture_data(gesture_name)
        elif choice == "2":
            train_model()
        elif choice == "3":
            gesture_name = input("Enter gesture name to delete: ")
            delete_gesture_data(gesture_name)
        elif choice == "4":
            delete_all_trained_data()
        elif choice == "5":
            break