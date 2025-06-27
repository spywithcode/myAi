import datetime
import requests
from voice_commands import speak

def get_weather():
    api_key = ""             # Replace with your OpenWeatherMap API key
    city = "indore"          # Replace with your city
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    
    try:
        response = requests.get(url)
        data = response.json()
        if data["cod"] == 200:
            temp = data["main"]["temp"]
            description = data["weather"][0]["description"]
            return f"The weather in {city} is {description} with a temperature of {temp} degrees Celsius."
        else:
            return "Sorry, I couldn't fetch the weather information."
    except Exception:
        return "Sorry, I couldn't fetch the weather information."

def greetMe():
    now = datetime.datetime.now()
    hour = now.hour

    if hour >= 0 and hour <= 12:
        print("Good Morning, Sir")
        speak("Good Morning, Sir")
        
    elif hour > 12 and hour <= 18:
        print("Good Afternoon, Sir")
        speak("Good Afternoon, Sir")
        
    else:
        print("Good Evening, Sir")
        speak("Good Evening, Sir")

    date_str = now.strftime("%A, %d %B %Y")
    time_str = now.strftime("%I:%M %p")
    
    print(f"Today is {date_str}. The current time is {time_str}.")
    speak(f"Today is {date_str}. The current time is {time_str}.")
    
    print(get_weather())
    speak(get_weather())
    
    print("Please tell me, How can I help you ?")
    speak("Please tell me, How can I help you ?")
