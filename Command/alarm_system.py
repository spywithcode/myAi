import speech_recognition as sr
import threading
import datetime
import pyttsx3
import time
import os

try:
    from playsound import playsound
except ImportError:
    playsound = None

ALARM_SOUND_FILE = "Command\\alarm.mp3"
SPEAKER_RATE = 150
SPEAKER_VOLUME = 1.0
SPEAKER_VOICE_ID = None

alarms = []
system_running = True
recognizer = sr.Recognizer()
engine = None

def speak(text):
    global engine
    if engine:
        print(f"Assistant: {text}")
        engine.say(text)
        engine.runAndWait()
    else:
        print(f"Assistant (TTS not ready): {text}")

def listen():
    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=1)
            speak("Listening...")
            print("Listening...")
            try:
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                text = recognizer.recognize_google(audio)
                print(f"You said: {text}")
                return text.lower()
            except sr.WaitTimeoutError:
                print("No speech detected within the timeout.")
                return ""
            except sr.UnknownValueError:
                speak("Sorry, I could not understand what you said.")
                return ""
            except sr.RequestError as e:
                speak(f"Could not request results from Google Speech Recognition service; {e}")
                return ""
    except OSError as e:
        speak("Microphone not found or not accessible. Please check your microphone connection and permissions.")
        print(f"Microphone error: {e}")
        return ""
    except Exception as e:
        speak(f"An unexpected error occurred during listening: {e}")
        print(f"Listening error: {e}")
        return ""

def set_alarm(command_text):
    now = datetime.datetime.now()
    alarm_time = None
    time_str = ""
    if "for" in command_text:
        time_str = command_text.split("for")[-1].strip()
    elif "at" in command_text:
        time_str = command_text.split("at")[-1].strip()
    elif "alarm" in command_text:
        parts = command_text.split("alarm", 1)
        if len(parts) > 1:
            time_str = parts[1].strip()
    time_str = time_str.replace("o'clock", "").replace("o clock", "").strip()
    try:
        if "am" in time_str:
            time_str = time_str.replace("am", "").strip()
            try:
                alarm_time = datetime.datetime.strptime(time_str, "%I:%M").replace(year=now.year, month=now.month, day=now.day)
            except ValueError:
                alarm_time = datetime.datetime.strptime(time_str, "%I").replace(year=now.year, month=now.month, day=now.day, minute=0)
        elif "pm" in time_str:
            time_str = time_str.replace("pm", "").strip()
            try:
                alarm_time = datetime.datetime.strptime(time_str, "%I:%M").replace(year=now.year, month=now.month, day=now.day)
            except ValueError:
                alarm_time = datetime.datetime.strptime(time_str, "%I").replace(year=now.year, month=now.month, day=now.day, minute=0)
            if alarm_time.hour < 12:
                alarm_time += datetime.timedelta(hours=12)
        elif time_str.isdigit() and (len(time_str) == 4 or len(time_str) == 3):
            if len(time_str) == 3:
                time_str = '0' + time_str
            hour = int(time_str[:2])
            minute = int(time_str[2:])
            alarm_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
        elif ":" in time_str:
            try:
                alarm_time = datetime.datetime.strptime(time_str, "%H:%M").replace(year=now.year, month=now.month, day=now.day)
            except ValueError:
                alarm_time = datetime.datetime.strptime(time_str, "%I:%M").replace(year=now.year, month=now.month, day=now.day)
        elif time_str.isdigit():
            hour = int(time_str)
            if 0 <= hour <= 23:
                alarm_time = now.replace(hour=hour, minute=0, second=0, microsecond=0)
            else:
                speak("Invalid hour specified. Please use an hour between 0 and 23.")
                return
    except ValueError:
        speak("I couldn't parse the time. Please say, for example, 'set an alarm for 7 PM', 'for 19:30', or 'at 7 o'clock'.")
        return
    except Exception as e:
        speak(f"An unexpected error occurred while setting the alarm: {e}")
        print(f"Time parsing error: {e}")
        return
    if alarm_time:
        if alarm_time <= now:
            alarm_time += datetime.timedelta(days=1)
            speak(f"That time is in the past. Alarm set for tomorrow at {alarm_time.strftime('%I:%M %p')}.")
        else:
            speak(f"Alarm set for {alarm_time.strftime('%I:%M %p')}.")
        alarms.append(alarm_time)
        alarms.sort()
    else:
        speak("I couldn't understand the time you specified. Please try again.")

def list_alarms():
    if not alarms:
        speak("You have no alarms set.")
    else:
        speak("Your current alarms are:")
        for i, alarm in enumerate(alarms):
            speak(f"Alarm {i+1}: {alarm.strftime('%I:%M %p on %A, %B %d')}")

def clear_alarms():
    global alarms
    if alarms:
        alarms = []
        speak("All alarms cleared.")
    else:
        speak("There are no alarms to clear.")

def play_alarm_sound():
    if playsound:
        if os.path.exists(ALARM_SOUND_FILE):
            try:
                playsound(ALARM_SOUND_FILE)
            except Exception as e:
                speak("There was an error playing the alarm sound.")
                print(f"Playsound error: {e}")
        else:
            speak("Alarm sound file not found. Please ensure 'Command\\alarm.mp3' is in the same directory.")
            print(f"Error: '{ALARM_SOUND_FILE}' not found.")
    else:
        speak("Alarm sound feature is not available. 'playsound' library not installed.")

def alarm_checker():
    global system_running
    while system_running:
        now = datetime.datetime.now()
        triggered_alarms = [a for a in alarms if now >= a]
        for alarm_time in triggered_alarms:
            speak(f"It's {alarm_time.strftime('%I:%M %p')}! Wake up, Shukla ji!")
            play_alarm_sound()
            alarms.remove(alarm_time)
        time.sleep(1)

def initialize_system():
    global engine
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', SPEAKER_RATE)
        engine.setProperty('volume', SPEAKER_VOLUME)
        if SPEAKER_VOICE_ID:
            voices = engine.getProperty('voices')
            found_voice = False
            for voice in voices:
                if voice.id == SPEAKER_VOICE_ID:
                    engine.setProperty('voice', voice.id)
                    found_voice = True
                    break
        speak("System initialized successfully.")
    except Exception as e:
        print(f"Error initializing TTS engine: {e}")
        engine = None
    checker_thread = threading.Thread(target=alarm_checker, daemon=True)
    checker_thread.start()

def main_loop():
    global system_running
    speak("Voice control alarm system activated. How can I help you, Shukla ji?")
    speak("You can say 'set an alarm for 7 PM', 'list alarms', or 'clear alarms'. Say 'exit' to quit.")
    while system_running:
        command = listen()
        if command:
            if "set an alarm for" in command or "wake me up at" in command or "alarm for" in command:
                set_alarm(command)
            elif "list alarms" in command or "what are my alarms" in command:
                list_alarms()
            elif "clear alarms" in command or "delete all alarms" in command or "remove all alarms" in command:
                clear_alarms()
            elif "exit" in command or "quit" in command or "goodbye" in command:
                speak("Shutting down the alarm system. Goodbye, Shukla ji!")
                system_running = False
            else:
                speak("I didn't understand that command. Please try again.")
        time.sleep(0.5)

if __name__ == "__main__":
    if not os.path.exists(ALARM_SOUND_FILE):
        print(f"WARNING: '{ALARM_SOUND_FILE}' not found. Please add the file to the script's directory for alarm sounds to work.")
        print(f"You can download a sample MP3 or create a silent one if you don't need a sound.")
    initialize_system()
    try:
        main_loop()
    except KeyboardInterrupt:
        speak("Alarm system interrupted by user.")
        print("Exiting system...")
    finally:
        system_running = False
        if engine:
            engine.stop()
        print("System shut down.")

