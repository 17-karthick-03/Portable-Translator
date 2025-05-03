# Portable Translator: ISL to Audio

A portable real-time translator that converts Indian Sign Language (ISL) gestures into audible speech using computer vision and machine learning. This project is designed to assist communication between deaf or non-verbal individuals and those unfamiliar with sign language.

## 🔧 Project Overview

- **Hardware:** Raspberry Pi Zero W, Camera Module, Bluetooth Earphones
- **Model:** Random Forest Classifier trained on custom ISL dataset
- **Frameworks/Libraries:** MediaPipe, OpenCV, Scikit-learn, Python Sockets
- **Classes Covered:** A–L, M–O, U–X, and custom gestures like 'Love'

## 📌 How It Works

1. The camera captures hand gestures.
2. MediaPipe extracts 21 hand landmarks.
3. Extracted features are sent via socket to a server (laptop).
4. A trained ML model classifies the sign.
5. The result is converted to speech and sent to Bluetooth audio.

## 📂 Project Structure

- `train_model/` – Scripts for feature extraction and model training
- `receiver/` – Laptop/server-side code for receiving data and predicting
- `client/` – Raspberry Pi code for capturing and sending gesture data
- `dataset/` – Custom ISL gesture dataset organized in folders
- `model.pkl` – Trained Random Forest model
- `README.md` – Project overview

## 📦 Installation & Usage

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/isl-audio-translator.git
   cd isl-audio-translator
