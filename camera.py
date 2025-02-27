import cv2
import mediapipe as mp
import numpy as np

class Camera:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
        self.mp_drawing = mp.solutions.drawing_utils

    def get_frame(self):
        """Capture a frame, process it, and return landmarks + image."""
        ret, frame = self.cap.read()
        if not ret:
            return None, None

        frame = cv2.flip(frame, 1)  # Flip for mirror effect
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = self.hands.process(rgb_frame)
        landmarks = results.multi_hand_landmarks

        return frame, landmarks

    def release(self):
        """Release the camera."""
        self.cap.release()
        cv2.destroyAllWindows()
