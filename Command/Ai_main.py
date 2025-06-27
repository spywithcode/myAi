#-------- Import PiP Section ----------
import os
import cv2
import time
import random
import datetime
import requests
import pyautogui
import webbrowser

# import speedtest
# import image_gen

# ---------- import File Section --------------
from pathlib import Path
from bs4 import BeautifulSoup
from voice_commands import speak, takeCommand 

# from pygame import mixer

# ====================================
def validate_password():
    """Prompt the user to enter the password and validate it."""
    password_file = Path(r"myAi\\Command\\password.txt")
    if not password_file.exists():
        print("Password file not found!")
        exit()

    with password_file.open("r") as pw_file:
        stored_password = pw_file.read().strip()

    for attempt in range(3):
        entered_password = input("Enter Password to open Jarvis :- ").strip()
        if entered_password == stored_password:
            print("WELCOME SIR! PLEASE SPEAK [START JARVIS] TO LOAD ME UP")
            return True
        elif attempt == 2:
            print("Too many failed attempts. Exiting.")
            exit()
        else:
            print("Incorrect password. Try again.")
    return False

# ====================================
def initialize_face_recognition():
    """Initialize face recognition components."""
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read(r"Face-Recognition\\trainer\\trainer.yml")
    cascade_path = r"Face-Recognition\\haarcascade_frontalface_default.xml"
    face_cascade = cv2.CascadeClassifier(cascade_path)
    return recognizer, face_cascade

def face_recognition_loop(recognizer, face_cascade):
    """Perform face recognition in a loop and save recognized face images."""
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cam.set(3, 640)
    cam.set(4, 480)

    min_w = 0.1 * cam.get(3)
    min_h = 0.1 * cam.get(4)

    # Ensure the 'data' folder exists
    if not os.path.exists("data"):
        os.makedirs("data")

    start_time = time.time()  # Record the start time

    while True:
        elapsed_time = time.time() - start_time  # Calculate elapsed time
        if elapsed_time > 30:  # Exit if 30 seconds have passed
            print("Face recognition timed out. Exiting.")
            speak("Face recognition timed out. Exiting.")
            break

        ret, img = cam.read()
        if not ret:
            print("Failed to capture image. Exiting.")
            break

        converted_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(
            converted_image, scaleFactor=1.2, minNeighbors=5, minSize=(int(min_w), int(min_h))
        )

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            id, accuracy = recognizer.predict(converted_image[y:y + h, x:x + w])

            if accuracy < 100:
                # Save the recognized face image
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")                
                face_image = img[y:y + h, x:x + w]
                save_path = f"data/face_{timestamp}.jpg"
                cv2.imwrite(save_path, face_image)
                print(f"Face image saved at: {save_path}")

                speak("Optical Face Recognition Done.")
                cam.release()
                cv2.destroyAllWindows()
                return True
            else:
                speak("Optical Face Recognition Failed")
                break

    cam.release()
    cv2.destroyAllWindows()
    return False

# ====================================
if __name__ == "__main__":
    
    print("Welcome sir! the voice-controlled jarvis system..!!")
    speak("Welcome sir! the voice-controlled jarvis system.")
    
    
    recognizer, face_cascade = initialize_face_recognition()
    if face_recognition_loop(recognizer, face_cascade):
        print("Face recognition successful. Starting JARVIS...!!")

        print("Please enter the password to start jarvis..!!")
        speak("Please enter the password to start jarvis")
        
        if validate_password():
            from INTRO import play_gif
            play_gif()


###############################################################################################
###############################################################################################
            
            # Add further JARVIS functionalities here...!!
            while True:
                query = takeCommand().lower()
                
                if "start" in query or "open" in query:
                    speak("Loading Jarvis, sir..!!")
                    from GreetMe import greetMe
                    greetMe()

                    
# ============================  START COMMANDS ===================================
# ================================================================================
                    
                    while True:
                        query = takeCommand().lower()
                        
#                       # ======== Go to sleep  =============

                        if "stop" in query:
                            speak("Ok sir , You can call me anytime")
                            break 
                        
                        # ======== Exit Jarvis =============
                        
                        elif "exit" in query:
                            import sys
                            speak("Exit, Sir")
                            sys.exit()
                            
                        # ======== Close Jarvis =============
                        
                        elif "end code" in query:
                            speak("Closing Jarvis, sir")
                            os.system("taskkill /f /im python.exe")
                            break
                        
                        # ======== Restart Jarvis =============
                        
                        elif "restart code" in query:
                            speak("Restarting Jarvis, sir")
                            os.system("taskkill /f /im python.exe")
                            os.startfile("Jarvis_main.py")
                            break

                        # ===== Just Talk =========

                        elif "hello" in query:
                            speak("Hello sir, how are you ?")

                        elif "i am fine" in query:
                            speak("that's great, sir")

                        elif "how are you" in query:
                            speak("Perfect, sir")

                        elif "thank you" in query:
                            speak("you are welcome, sir")

                        # ===== Password =========

                        elif "change password" in query:
                            speak("What's the new password")
                            new_pw = input("Enter the new password ::\n")
                            new_password = open("password.txt","w")
                            new_password.write(new_pw)
                            new_password.close()
                            speak("Done sir")
                            speak(f"Your new password is{new_pw}")

                        # ===== Current Time  =======

                        elif "current time" in query or "time" in query:
                            strTime = datetime.datetime.now().strftime("%H:%M")
                            print(f"{strTime}")
                            speak(f"Sir, the time is {strTime}")

                        # ===== Current Date  =======

                        elif "current date" in query or "date" in query:
                            strDate = datetime.datetime.now().strftime("%d:%m")
                            print(f"{strDate}")
                            speak(f"Sir, the date is {strDate}")

                        # ===== Current Day  =======
                        
                        elif "current day" in query or "day" in query:
                            strDay = datetime.datetime.now().strftime("%A")
                            print(f"{strDay}")
                            speak(f"Sir, today is {strDay}")
                            
                        # ===== open Weather =======

                        elif "open weather" in query:
                            search = "temperature in delhi"
                            url = f"https://www.google.com/search?q={search}"
                            r = requests.get(url)
                            data = BeautifulSoup(r.text, "html.parser")
                            temp_div = data.find("div", class_="BNeawe")
                            if temp_div:
                                temp = temp_div.text
                                speak(f"Current {search} is {temp}")
                            else:
                                speak("Sorry, I couldn't fetch the weather information right now.")
                            
                        # ===== Video Pause  =======

                        elif "pause" in query:
                            pyautogui.press("k")
                            speak("video paused")

                        # ===== Video Play  =======

                        elif "play" in query:
                            pyautogui.press("k")
                            speak("video played")

                        # ===== Video Mute  =======

                        elif "mute" in query:
                            pyautogui.press("m")
                            speak("video muted")
                            
                        # ===== Video volume up  =======

                        elif "volume up" in query:
                            from keyboard import volumeup
                            speak("Turning volume up, sir")
                            volumeup()

                        # ======= Video volume Down  ======= 

                        elif "volume down" in query:
                            from keyboard import volumedown
                            speak("Turning volume down, sir")
                            volumedown()
                            
                        # ======= Video Next  ==========
                        
                        elif "next" in query:
                            from keyboard import nextsong
                            speak("Next video, sir")
                            pyautogui.press("l")
                            nextsong()
                            
                        # ===== Video Previous  =======
                        
                        elif "previous" in query:
                            from keyboard import previoussong
                            speak("Previous video, sir")
                            pyautogui.press("j")
                            previoussong()
                            
                        # ===== Video Fullscreen  =======
                        
                        elif "full mscreen" in query:
                            pyautogui.press("f")
                            speak("Video is in fullscreen mode, sir")
                            
                        # ====== Screenshot ==============
                        elif "screenshot" in query:
                            speak("Taking screenshot, sir")
                            myScreenshot = pyautogui.screenshot()
                            myScreenshot.save(r"screenshot\screenshot_{}.png".format(datetime.datetime.now().strftime('%H%M%S')))
                            speak("Screenshot saved on Folder, sir")
                            
                        # ======== Open Camera ==============
                        elif "camera" in query or "webcam" in query:
                            speak("Opening camera, sir")
                            cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
                            while True:
                                ret, frame = cam.read()
                                if not ret:
                                    speak("Failed to open camera, sir")
                                    break
                                cv2.imshow("Camera", frame)
                                if cv2.waitKey(1) & 0xFF == ord('q'):
                                    break
                            cam.release()
                            cv2.destroyAllWindows()
                            
                        # ========== Take a Photo ==============
                        elif "take a photo" in query or "capture" in query:
                            speak("Taking a photo, sir")
                            cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
                            ret, frame = cam.read()
                            if ret:
                                speak("Please Smile, sir")
                                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                                photo_path = f"photos/photo_{timestamp}.jpg"
                                cv2.imwrite(photo_path, frame)
                                speak(f"Photo saved at {photo_path}, sir")
                            else:
                                speak("Failed to take a photo, sir")
                            cam.release()
                            cv2.destroyAllWindows()
                            
                            
                        # ========= I am Tired  =======
                        
                        elif "tired" in query or "sleepy" in query:
                            speak("Playing your favourite songs, sir")
                            a = (1,2,3,4)
                            song = random.choice(a)
                            if song == 1:
                                webbrowser.open("https://youtu.be/cQM55aOrZCg?si=ig6GbMW0gOVU72Lc")
                            elif song == 2:
                                webbrowser.open("https://youtu.be/2eliQ_KR8yA?si=THFPkgb6AeLr8-Am")
                            elif song == 3:
                                webbrowser.open("https://youtu.be/Nd3PmNWqpPQ?si=laStc5TPnuIhLItP")
                            elif song == 4:
                                webbrowser.open("https://youtu.be/Nd3PmNWqpPQ?si=y3ys3ngv2hwbyRY9")
                                
                        # =========== Favorite Applications  ==========
                        elif "open all applications" in query or "open all my favorite applications" in query:
                            speak("Opening all applications, sir")
                            apps = [
                                "https://chatgpt.com/",
                                "https://www.canva.com/",
                                "https://www..com/",
                                "https://gemini.google.com/app",
                                "https://www.linkedin.com/in/sandeep-shukla-b87610302/"
                            ]
                            for app in apps:
                                webbrowser.open(app)

                        # ============ Open Apps ==============
                        elif "open apps" in query:
                            speak("Opening application, sir")
                            from Dictapp import openappweb
                            openappweb()
                            
                        # ============ Close Apps ==============
                        elif "close" in query:
                            speak("Closing application, sir")
                            from Dictapp import closeappweb
                            closeappweb()
                            
                        # ============ Open Web ==============
                        elif "open web" in query:
                            speak("Opening web, sir")
                            from Dictapp import openappweb
                            openappweb()
                            
                        # ============ Close Tabs ==============
                        elif "close tabs" in query or "close tab" in query:
                            speak("Closing tabs, sir")
                            from Dictapp import closeappweb
                            closeappweb()
                            
                        # ============ Open File Explorer ==============
                        elif "open file explorer" in query or "explorer" in query:
                            speak("Opening File Explorer, sir")
                            os.startfile(os.path.expanduser("~\\Documents"))
                            
                        # ============ Open Downloads Folder ==============
                        elif "open downloads file" in query or "download" in query:
                            speak("Opening Downloads folder, sir")
                            os.startfile(os.path.expanduser("~\\Downloads"))
                        

# ========================================================================================
# ================================= END COMMAND ==========================================

                        # ====== Shutdown =============
                        
                        elif "shutdown" in query:
                            speak("Shutting down, sir")
                            os.system("shutdown /s /t 1")

                        # ====== Restart ==============
                        
                        elif "restart" in query:
                            speak("Restarting, sir")
                            os.system("shutdown /r /t 1")
                            
                        elif "sleep" in query:
                            speak("Sleep, sir")
                            pyautogui.press("win+l")
                            
                        # ====== Lock ==============
                        elif "lock" in query:
                            speak("Locking the computer, sir")
                            os.system("rundll32.exe user32.dll,LockWorkStation")

##########################################################################################
##########################################################################################


                        # ====== Log off ==============
                        
                        elif "log off" in query:
                            speak("Logging off, sir")
                            os.system("shutdown -l")

                        # ====== Open Notepad ==============
                        elif "notepad" in query:
                            speak("Opening Notepad, sir")
                            os.startfile(r"C:\Windows\System32\notepad.exe")

                        # ====== Open Command Prompt ==============
                        elif "command prompt" in query or "cmd" in query:
                            speak("Opening Command Prompt, sir")
                            os.startfile(r"C:\Windows\System32\cmd.exe")

                        # ====== Open Calculator ==============
                        elif "calculator" in query or "calc" in query:
                            speak("Opening Calculator, sir")
                            os.startfile(r"C:\Windows\System32\calc.exe")

                        # ====== Open Paint ==============
                        elif "paint" in query or "ms paint" in query:
                            speak("Opening Paint, sir")
                            os.startfile(r"C:\Windows\System32\mspaint.exe")

                        # ====== Open Microsoft Word ==============
                        elif "word" in query or "ms word" in query:
                            speak("Opening Microsoft Word, sir")
                            os.startfile(r"C:\Program Files (x86)\Microsoft Office\root\Office16\WINWORD.EXE")

                        # ====== Open Microsoft Excel ==============
                        elif "excel" in query or "ms excel" in query:
                            speak("Opening Microsoft Excel, sir")
                            os.startfile(r"C:\Program Files (x86)\Microsoft Office\root\Office16\EXCEL.EXE")

                        # ====== Open Microsoft PowerPoint ==============
                        elif "powerpoint" in query or "ms powerpoint" in query:
                            speak("Opening Microsoft PowerPoint, sir")
                            os.startfile(r"C:\Program Files (x86)\Microsoft Office\root\Office16\POWERPNT.EXE")
                            