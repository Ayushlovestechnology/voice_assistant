import speech_recognition as sr
import pyttsx3
import pywhatkit
import wikipedia
import requests
import pyjokes
from datetime import datetime

# Initialize the speech engine
engine = pyttsx3.init()

def speak(text):
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()

def listen():
    """Listen for a voice command and convert it to text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            print(f"User said: {command}\n")
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
            command = ""
        except sr.RequestError:
            print("Sorry, my speech service is down.")
            command = ""
        return command.lower()

def get_weather(city):
    """Get the current weather for a given city."""
    api_key = '0d8006ff0bbc9ba502009d30e4861244'
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "q=" + city + "&appid=" + api_key
    response = requests.get(complete_url)
    data = response.json()
    if data["cod"] != "404":
        main = data["main"]
        temperature = main["temp"]
        weather_description = data["weather"][0]["description"]
        speak(f"The temperature in {city} is {temperature - 273.15:.2f} degrees Celsius with {weather_description}")
    else:
        speak("City not found")

def handle_command(command):
    """Handle the voice command."""
    if 'play' in command:
        song = command.replace('play', '')
        speak(f'Playing {song}')
        pywhatkit.playonyt(song)
    elif 'search for' in command:
        query = command.replace('search for', '')
        speak(f'Searching for {query}')
        info = wikipedia.summary(query, sentences=2)
        speak(info)
    elif 'time' in command:
        now = datetime.now().strftime("%H:%M")
        speak(f"The time is {now}")
    elif 'joke' in command:
        joke = pyjokes.get_joke()
        speak(joke)
    elif 'weather in' in command:
        city = command.replace('weather in', '').strip()
        get_weather(city)
    else:
        speak("I did not understand the command")

if __name__ == "__main__":
    speak("Hello, how can I assist you today?")
    while True:
        command = listen()
        if command:
            handle_command(command)
