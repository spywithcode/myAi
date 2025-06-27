import cv2

recognizer = cv2.face.LBPHFaceRecognizer_create()   # Local Binary Patterns Histograms
recognizer.read('Face-Recognition/trainer/trainer.yml')              #load trained model
cascadePath = "Face-Recognition/haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath)    #initializing haar cascade for object detection approach

font = cv2.FONT_HERSHEY_SIMPLEX                     #denotes the font type


id = 2                                          #number of persons you want to Recognize


names = ['','avi']                              #names, leave first empty bcz counter starts from 0


cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)        #cv2.CAP_DSHOW to remove warning
cam.set(3, 640)                                 # set video FrameWidht
cam.set(4, 480)                                 # set video FrameHeight

# Define min window size to be recognized as a face
minW = 0.1*cam.get(3)
minH = 0.1*cam.get(4)

# flag = True

while True:

    ret, img =cam.read()                        #read the frames using the above created object

    converted_image = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)  #The function converts an input image from one color space to another

    faces = faceCascade.detectMultiScale( 
        converted_image,
        scaleFactor = 1.2,
        minNeighbors = 5,
        minSize = (int(minW), int(minH)),
       )

    for(x,y,w,h) in faces:

        cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2) #used to draw a rectangle on any image

        id, accuracy = recognizer.predict(converted_image[y:y+h,x:x+w]) #to predict on every single image

        # Check if accuracy is less them 100 ==> "0" is perfect match 
        if (accuracy < 100):
            id = names[id]
            accuracy = "  {0}%".format(round(100 - accuracy))

        else:
            id = "unknown"
            accuracy = "  {0}%".format(round(100 - accuracy))
        
        cv2.putText(img, str(id), (x+5,y-5), font, 1, (255,255,255), 2)
        cv2.putText(img, str(accuracy), (x+5,y+h-5), font, 1, (255,255,0), 1)  
    
    cv2.imshow('camera',img) 

    k = cv2.waitKey(10) & 0xff                      # Press 'ESC' for exiting video
    if k == 27:
        break

# Do a bit of cleanup
print("Thanks for using this program, have a good day.")
cam.release()
cv2.destroyAllWindows()



# ==================================

# import cv2
# import sys
# import os

# # Paths
# CASCADE_PATH = "Face-Recognition/haarcascade_frontalface_default.xml"
# TRAINER_PATH = "Face-Recognition/trainer/trainer.yml"

# # Check if files exist
# if not os.path.exists(CASCADE_PATH):
#     print(f"Error: Cascade file '{CASCADE_PATH}' not found.")
#     sys.exit(1)
# if not os.path.exists(TRAINER_PATH):
#     print(f"Error: Trainer file '{TRAINER_PATH}' not found.")
#     sys.exit(1)

# # Initialize recognizer and cascade
# recognizer = cv2.face.LBPHFaceRecognizer_create()
# recognizer.read(TRAINER_PATH)
# face_cascade = cv2.CascadeClassifier(CASCADE_PATH)
# font = cv2.FONT_HERSHEY_SIMPLEX

# # Names list (index 0 is unused)
# names = ['', 'avi']

# # Open camera
# cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
# cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
# cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# minW = 0.1 * cam.get(cv2.CAP_PROP_FRAME_WIDTH)
# minH = 0.1 * cam.get(cv2.CAP_PROP_FRAME_HEIGHT)

# try:
#     while True:
#         ret, img = cam.read()
#         if not ret:
#             print("Failed to grab frame")
#             break

#         gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#         faces = face_cascade.detectMultiScale(
#             gray,
#             scaleFactor=1.2,
#             minNeighbors=5,
#             minSize=(int(minW), int(minH))
#         )

#         for (x, y, w, h) in faces:
#             cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
#             id_, confidence = recognizer.predict(gray[y:y + h, x:x + w])

#             if confidence < 100:
#                 name = names[id_] if id_ < len(names) else "unknown"
#                 label = f"{name}  {round(100 - confidence)}%"
#             else:
#                 label = "unknown  {0}%".format(round(100 - confidence))

#             cv2.putText(img, label, (x + 5, y - 5), font, 1, (255, 255, 255), 2)

#         cv2.imshow('camera', img)
#         if cv2.waitKey(10) & 0xFF == 27:  # ESC to exit
#             break
# finally:
#     print("Thanks for using this program, have a good day.")
#     cam.release()
#     cv2.destroyAllWindows()