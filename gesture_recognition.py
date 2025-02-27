import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import os

class GestureRecognition:
    def __init__(self, model_path="model/gesture_model.h5"):
        self.model_path = model_path
        self.model = self._load_or_create_model()

    def _load_or_create_model(self):
        """Load the trained model or create a new one if not found."""
        if os.path.exists(self.model_path):
            print("Loading existing model...")
            return tf.keras.models.load_model(self.model_path)
        else:
            print("No existing model found. Creating a new model...")
            return self._create_model()

    def _create_model(self, num_classes=5):
        """Define and compile a new neural network model."""
        model = Sequential([
        tf.keras.layers.Input(shape=(21 * 3,)),  # ✅ Use Input() properly
        Dense(128, activation='relu'),
        Dense(64, activation='relu'),
        Dense(32, activation='relu'),
        Dense(num_classes, activation='softmax')  # ✅ Ensure correct output size
            ])
        model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
        return model

    def predict_gesture(self, landmarks):
        """Predicts gesture based on hand landmarks."""
        if landmarks is None:
            return None

        input_data = np.array(landmarks).flatten().reshape(1, -1)
        prediction = self.model.predict(input_data, verbose=0)
        
        gesture_id = np.argmax(prediction)
        confidence = np.max(prediction)

        return gesture_id if confidence > 0.7 else None  # ✅ Use confidence threshold


    def save_model(self):
        """Saves the trained model."""
        self.model.save(self.model_path)
