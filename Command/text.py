from playsound import playsound
import os

ALARM_SOUND_FILE = 'Command\\alarm.mp3'

if os.path.exists(ALARM_SOUND_FILE):
    playsound(ALARM_SOUND_FILE)
    print("Sound played!")
else:
    print(f"Error: '{ALARM_SOUND_FILE}' not found in the current folder.")