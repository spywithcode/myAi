# import cv2
# import numpy as np
# from PIL import Image #pillow package
# import os

# path = 'samples' # Path for samples already taken

# recognizer = cv2.face.LBPHFaceRecognizer_create() # Local Binary Patterns Histograms
# detector = cv2.CascadeClassifier("Face-Recognition/haarcascade_frontalface_default.xml")
# #Haar Cascade classifier is an effective object detection approach


# def Images_And_Labels(path): # function to fetch the images and labels

#     imagePaths = [os.path.join(path,f) for f in os.listdir(path)]     
#     faceSamples=[]
#     ids = []

#     for imagePath in imagePaths: # to iterate particular image path

#         gray_img = Image.open(imagePath).convert('L') # convert it to grayscale
#         img_arr = np.array(gray_img,'uint8') #creating an array

#         id = int(os.path.split(imagePath)[-1].split(".")[1])
#         faces = detector.detectMultiScale(img_arr)

#         for (x,y,w,h) in faces:
#             faceSamples.append(img_arr[y:y+h,x:x+w])
#             ids.append(id)

#     return faceSamples,ids

# print ("Training faces. It will take a few seconds. Wait ...")

# faces,ids = Images_And_Labels(path)
# recognizer.train(faces, np.array(ids))

# recognizer.write('trainer/trainer.yml')  # Save the trained model as trainer.yml

# print("Model trained, Now we can recognize your face.")


# # ==================================



import cv2
import numpy as np
from PIL import Image
import os

SAMPLES_PATH = 'samples'
CASCADE_PATH = "Face-Recognition/haarcascade_frontalface_default.xml"
TRAINER_DIR = 'trainer'
TRAINER_PATH = os.path.join(TRAINER_DIR, 'trainer.yml')

def get_images_and_labels(path, detector):
    image_paths = [os.path.join(path, f) for f in os.listdir(path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    face_samples = []
    ids = []

    for image_path in image_paths:
        try:
            gray_img = Image.open(image_path).convert('L')
            img_arr = np.array(gray_img, 'uint8')
            # Assumes filename format: User.id.number.jpg
            id_str = os.path.split(image_path)[-1].split(".")[1]
            id = int(id_str)
            faces = detector.detectMultiScale(img_arr)
            for (x, y, w, h) in faces:
                face_samples.append(img_arr[y:y+h, x:x+w])
                ids.append(id)
        except Exception as e:
            print(f"Error processing {image_path}: {e}")

    return face_samples, ids

def main():
    if not os.path.exists(SAMPLES_PATH):
        print(f"Samples path '{SAMPLES_PATH}' does not exist.")
        return

    if not os.path.exists(CASCADE_PATH):
        print(f"Cascade file '{CASCADE_PATH}' not found.")
        return

    if not os.path.exists(TRAINER_DIR):
        os.makedirs(TRAINER_DIR)

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    detector = cv2.CascadeClassifier(CASCADE_PATH)

    print("Training faces. This may take a few seconds. Please wait...")

    faces, ids = get_images_and_labels(SAMPLES_PATH, detector)
    if faces and ids:
        recognizer.train(faces, np.array(ids))
        recognizer.write(TRAINER_PATH)
        print(f"Model trained and saved to '{TRAINER_PATH}'.")
    else:
        print("No faces or IDs found. Training aborted.")

if __name__ == "__main__":
    main()