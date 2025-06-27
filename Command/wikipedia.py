# wikipedia

import wikipedia
from voice_commands import takeCommand, speak

def searchWikipedia(query):
    speak("Searching from wikipedia....")
    query = takeCommand().lower()
    Results = wikipedia.summary(query,sentences = 2)
    speak("According to wikipedia..")
    print(Results)
    speak(Results)