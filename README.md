# GestureX - Transforming Motions into Commands
 
GestureX is an advanced AI-driven project that enables users to control their PC using hand gestures. From navigating slides to controlling volume and executing custom commands, GestureX brings touchless interaction to your system using deep learning-based gesture recognition.

---

## 🚀 Features

- 🎮 **Gesture-Based PC Control** – Perform actions like volume control, slide navigation, and more.
- 🎥 **Real-Time Camera Feed** – Live camera feed with overlayed gesture recognition.
- 🧠 **Deep Learning Model** – Utilizes a neural network with ReLU & Softmax for gesture classification.
- 🛠 **Custom Gesture Mapping** – Train your own gestures and map them to system commands.
- 🗑 **Data & Model Management** – Delete gesture datasets and trained model data as needed.
- 🕒 **Execution Threshold** – Prevents unintended repeated command execution.
- 🔧 **Custom CMD Commands** – Assign any CMD command to a gesture for ultimate flexibility.

---

## 📸 Demo

![GestureX Demo](https://your-image-link-here.com/demo.gif)  

---

## 🏗 Project Structure

```
GestureX/
│── dataset/               
│── model/                 # Trained deep learning models
│── camera.py              # Gesture image collection
│── gesture_control.py     # Maps gestures to system commands
│── gesture_recognition.py # Recognises user gesture using deep neural network
│── gesture_training.py    # Training script for custom gestures
│── gui.py                 # Make GUI using tkinter
│── main.py                # main 
│── requirements.txt       # Dependencies
│── README.md              # Documentation
```

---

## 🛠 Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/the-shreyashmaurya/GestureX.git
   cd GestureX
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run GestureX**:
   ```bash
   python main.py
   ```

---

## 📌 Usage Guide

### 🏗 Training a New Gesture

1. Train the model with new gestures:
   ```bash
   python gesture_training.py
   ```

### 🖥️ Mapping Gestures to Commands
  ```bash
   python gesture_control.py
   ```

---

## 🏆 Contributing

We welcome contributions! If you’d like to improve GestureX, feel free to fork the repository and create a pull request.

---

## 📄 License

See `LICENSE` for details.


