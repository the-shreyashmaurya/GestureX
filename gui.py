import tkinter as tk
from PIL import Image, ImageTk
import cv2
import numpy as np
from camera import Camera
from gesture_recognition import GestureRecognition
from gesture_control import execute_command
import json
import os

DATASET_PATH = "dataset/gesture_data.json"


class GestureGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Gesture Control")
        self.root.geometry("640x480")
        self.root.attributes("-topmost", True)
        self.root.configure(bg="black")

        self.label = tk.Label(self.root)
        self.label.pack()

        self.status_label = tk.Label(self.root, text="Gesture: None", fg="white", bg="black", font=("Arial", 12))
        self.status_label.pack()

        self.close_button = tk.Button(self.root, text="Close", command=self.close_app, bg="red", fg="white")
        self.close_button.pack()

        self.camera = Camera()
        self.recognizer = GestureRecognition()

        self.update_camera()
        self.root.mainloop()

    def update_camera(self):
        """Captures a frame, detects gestures, and updates GUI with bounding box & text."""
        frame, landmarks = self.camera.get_frame()
        if frame is not None:
            h, w, _ = frame.shape  # Get frame dimensions

            if landmarks:
                for hand_landmarks in landmarks:
                    landmark_list = [[lm.x, lm.y, lm.z] for lm in hand_landmarks.landmark]
                    gesture_id = self.recognizer.predict_gesture(landmark_list)

                    if gesture_id is not None:
                        gesture_name = self.get_gesture_name(gesture_id)
                        self.status_label.config(text=f"Gesture: {gesture_name}")
                        execute_command(gesture_name)

                        # Get bounding box around hand
                        x_min = min([lm.x for lm in hand_landmarks.landmark]) * w
                        y_min = min([lm.y for lm in hand_landmarks.landmark]) * h
                        x_max = max([lm.x for lm in hand_landmarks.landmark]) * w
                        y_max = max([lm.y for lm in hand_landmarks.landmark]) * h

                        # Draw bounding box
                        cv2.rectangle(frame, (int(x_min), int(y_min)), (int(x_max), int(y_max)), (0, 255, 0), 2)

                        # Display gesture name near bounding box
                        cv2.putText(frame, gesture_name, (int(x_min), int(y_min) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

                        # Draw hand landmarks
                        for lm in hand_landmarks.landmark:
                            cx, cy = int(lm.x * w), int(lm.y * h)
                            cv2.circle(frame, (cx, cy), 5, (0, 255, 255), -1)

            # Convert frame for Tkinter display
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            self.label.imgtk = imgtk
            self.label.configure(image=imgtk)

        self.root.after(10, self.update_camera)
    def get_gesture_name(self, gesture_id):
        """Dynamically retrieves gesture name from dataset instead of manual mapping."""
        if not os.path.exists(DATASET_PATH):
            return "Unknown"

        with open(DATASET_PATH, "r") as f:
            data = json.load(f)

        gesture_classes = data.get("classes", {})

        # Find gesture name by its ID
        for name, id in gesture_classes.items():
            if id == gesture_id:
                return name

        return "Unknown"

    def close_app(self):
        """Closes the application."""
        self.camera.release()
        self.root.destroy()

if __name__ == "__main__":
    GestureGUI()
