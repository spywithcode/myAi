# ||Professional Data Scientist || Expert in Python , SQL, AWS , Excel || Data Analyst || Data Pipeline || Django || Flask || PowerBI || AWS Glue

import speech_recognition as sr
import mtranslate
import pyttsx3
import os

# Initialize text-to-speech engine
engine = pyttsx3.init("sapi5")
engine.setProperty("voice", engine.getProperty("voices")[1].id)
engine.setProperty("rate", 200)

def speak(audio):
    """Convert text to speech and speak it out loud."""
    try:
        engine.say(audio)
        engine.runAndWait()
    except Exception as e:
        print(f"Error in translation: {e}")

def takeCommand():
    """Listen for a command and return it as a string."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        r.energy_threshold = 300
        audio = r.listen(source)

    try:
        print("Understanding...")
        query = r.recognize_google(audio, language='en-in')
        query = mtranslate.translate(query, to_language="en-in")
        print(f"You Said: {query}\n")
    except Exception as e:
        print("Say that again..")
        return "None"
    return query
