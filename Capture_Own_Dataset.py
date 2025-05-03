import os
import cv2
import time
    
# Define dataset path and letter
dataset_path = "path/to/the/directory/data"
letter = "Sign-Language-Name"  # Change this for different letters

# Create folder if not exists
letter_folder = os.path.join(dataset_path, letter)
os.makedirs(letter_folder, exist_ok=True)

# OpenCV camera setup (Use external USB camera)
cap = cv2.VideoCapture(1)  # Change to 1 for USB camera, try 2 if it doesn't work

# Check if the camera is opened
if not cap.isOpened():
    print("⚠️ Unable to access the external USB camera. Trying default camera...")
    cap = cv2.VideoCapture(0)  # Fallback to built-in laptop camera

print("Press 'q' to start capturing images in 2 seconds...")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to access the camera.")
        break

    cv2.imshow("USB Camera View (Press 'q' to Start)", frame)

    # Wait for user to press 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("Starting capture in 2 seconds...")
        time.sleep(4)
        break

# Capture 300 images
for i in range(1, 301):
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture frame.")
        continue

    filename = f"{letter}_{i:03d}.jpg"  # Example: Hello_001.jpg to Hello_300.jpg
    filepath = os.path.join(letter_folder, filename)

    # Save image
    cv2.imwrite(filepath, frame)
    print(f"Captured: {filename}")

    time.sleep(0.05)  # Small delay to avoid rapid captures

print("✅ Image collection complete!")
cap.release()
cv2.destroyAllWindows()
