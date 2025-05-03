import pickle
import cv2
import mediapipe as mp
import numpy as np
import socket
import os
import time

# Load Trained Model
model_dict = pickle.load(open('./model.p', 'rb'))
model = model_dict['model']
expected_features = model.n_features_in_

# Define Image Folder
frame_folder = "path/to/the/directory/PiFrames"

# MediaPipe Hand Detection Setup
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)

# Class Labels
labels_dict = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'I',.............}

# Socket Server Setup
server_ip = "Change-to-your-Laptor's-IP" 
server_port = 5000
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((server_ip, server_port))
server_socket.listen(1)

print("[INFO] Waiting for connection from Raspberry Pi...")

def predict_sign(image_path):
    try:
        # Wait for file to appear (Max 5 sec)
        wait_time = 0
        while not os.path.exists(image_path) and wait_time < 5:
            time.sleep(0.5)
            wait_time += 0.5

        if not os.path.exists(image_path):
            print(f"[ERROR] File not found after waiting: {image_path}")
            return "Error: File Not Found"

        # Load and Process Image
        img = cv2.imread(image_path)
        if img is None:
            print("[ERROR] Unable to load image.")
            return "Error: Invalid Image"

        H, W, _ = img.shape
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(img_rgb)

        if not results.multi_hand_landmarks:
            return "Null"

        data_aux, x_, y_ = [], [], []
        for hand_landmarks in results.multi_hand_landmarks:
            for i in range(len(hand_landmarks.landmark)):
                x = hand_landmarks.landmark[i].x
                y = hand_landmarks.landmark[i].y
                x_.append(x)
                y_.append(y)

            for i in range(len(hand_landmarks.landmark)):
                data_aux.append(hand_landmarks.landmark[i].x - min(x_))
                data_aux.append(hand_landmarks.landmark[i].y - min(y_))

        # Ensure feature vector matches model input
        if len(data_aux) < expected_features:
            data_aux += [0] * (expected_features - len(data_aux))
        data_aux = np.array(data_aux).reshape(1, -1)

        prediction = model.predict(data_aux)
        predicted_value = prediction[0]

        # Handling different prediction formats
        if isinstance(predicted_value, str):
            predicted_label = predicted_value  # Directly use it
        elif isinstance(predicted_value, (int, np.integer)):
            predicted_label = labels_dict.get(int(predicted_value), "Unknown")
        else:
            predicted_label = "Unknown"

        return predicted_label
    except Exception as e:
        print(f"[ERROR] Exception during prediction: {e}")
        return "Error: Exception Occurred"

while True:
    try:
        conn, addr = server_socket.accept()
        print(f"[INFO] Connected by {addr}")

        # Receive image filename from Raspberry Pi
        filename = conn.recv(1024).decode().strip()
        print(f"[INFO] Received filename: '{filename}'")

        # Predict the class
        image_path = os.path.join(frame_folder, filename)
        prediction = predict_sign(image_path)
        print(f"[INFO] Predicted sign: {prediction}")

        # Send prediction back to Raspberry Pi
        conn.sendall(prediction.encode())
        conn.close()
    except Exception as e:
        print(f"[ERROR] Server loop exception: {e}")
        break

server_socket.close()
