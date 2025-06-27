import cv2
import os

def initialize_camera():
    """Initialize the webcam and set frame dimensions."""
    camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    camera.set(3, 640)  # Set video frame width
    camera.set(4, 480)  # Set video frame height
    return camera

def create_directory(directory):
    """Create a directory if it doesn't exist."""
    if not os.path.exists(directory):
        os.makedirs(directory)

def capture_samples(face_id, output_dir="samples", sample_count=10):
    """
    Capture face samples using the webcam.
    
    Args:
        face_id (str): Unique numeric ID for the user.
        output_dir (str): Directory to save the captured samples.
        sample_count (int): Number of samples to capture.
    """
    # Initialize the camera and face detector
    camera = initialize_camera()
    face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    print("Taking samples, look at the camera...")
    count = 0  # Counter for the number of samples taken

    while True:
        ret, frame = camera.read()  # Capture a frame from the webcam
        if not ret:
            print("Failed to capture image. Exiting...")
            break

        # Convert the frame to grayscale for face detection
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(gray_frame, scaleFactor=1.3, minNeighbors=5)

        for (x, y, w, h) in faces:
            # Draw a rectangle around the detected face
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            count += 1

            # Save the captured face image to the output directory
            create_directory(output_dir)
            face_image_path = os.path.join(output_dir, f"face.{face_id}.{count}.jpg")
            cv2.imwrite(face_image_path, gray_frame[y:y + h, x:x + w])

            # Display the frame with the rectangle
            cv2.imshow('Face Capture', frame)

        # Wait for a key press and check for exit conditions
        key = cv2.waitKey(100) & 0xFF
        if key == 27:  # Press 'ESC' to exit
            print("ESC pressed. Exiting...")
            break
        elif count >= sample_count:  # Stop after capturing the required number of samples
            print(f"Captured {sample_count} samples. Exiting...")
            break

    # Release the camera and close all OpenCV windows
    camera.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # Prompt the user for a numeric face ID
    while True:
        face_id = input("Enter a numeric user ID here: ")
        if face_id.isdigit():
            break
        else:
            print("Invalid input. Please enter a numeric ID.")

    # Start capturing samples
    capture_samples(face_id)
