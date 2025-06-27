import os
import pyautogui
import webbrowser
import pyttsx3
from time import sleep
from voice_commands import takeCommand, speak

SPEECH_RATE = 200

engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)
engine.setProperty("rate", SPEECH_RATE)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def open_app(app_name):
    try:
        os.system(f"C:/Windows/System32/{app_name}")
    except Exception as e:
        speak(f"Error opening {app_name}: {str(e)}")

def close_app(app_name):
    try:
        os.system(f"taskkill /f /im {app_name}.exe")
    except Exception as e:
        speak(f"Error closing {app_name}: {str(e)}")

def open_web(query):
    try:
        webbrowser.open(f"https://www.{query}")
    except Exception as e:
        speak(f"Error opening {query}: {str(e)}")

def close_tabs(num_tabs):
    for _ in range(num_tabs):
        pyautogui.hotkey("ctrl+w")
        sleep(0.5)

dictapp = {
    "commandprompt": "cmd",
    "paint": "paint",
    "word": "winword",
    "excel": "excel",
    "chrome": "chrome",
    "vscode": "code",
    "powerpoint": "powerpnt"
}

def closeappweb():
    speak("What should I close, sir?")
    query = takeCommand().lower()
    if "tab" in query or "Tab" in query:
        speak("How many tabs should I close, sir?")
        query = takeCommand().lower()
        if "all" in query:
            speak("Closing all tabs, sir")
            close_tabs(100)
        else:
            try:
                speak("Closing tab, sir")
                num_tabs = int(''.join(filter(str.isdigit, query)))
                close_tabs(num_tabs)
            except ValueError:
                speak("Sorry, I couldn't understand the number of tabs.")
    else:
        for app, exe in dictapp.items():
            if app in query:
                speak("Closing app, sir")
                close_app(exe)

def openappweb():
    speak("What should I open, sir?")
    query = takeCommand().lower()
    speak("Launching, sir")
    if any(ext in query for ext in [".com", ".co.in", ".org"]):
        open_web(query)
    else:
        for app, exe in dictapp.items():
            if app in query:
                open_app(exe)


    