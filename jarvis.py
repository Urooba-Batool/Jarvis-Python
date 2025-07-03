import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import pywhatkit
import os

# Initialize text-to-speech engine
engine = pyttsx3.init()

def speak(text):
    """Speak the given text."""
    engine.say(text)
    engine.runAndWait()

def listen():
    """Listen to user commands via microphone."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.pause_threshold = 1
        try:
            command = recognizer.listen(source)
            query = recognizer.recognize_google(command, language='en')
            print(f"You said: {query}")
            return query.lower()
        except sr.UnknownValueError:
            speak("Sorry, I didn't understand that. Could you repeat?")
            return None
        except sr.RequestError:
            speak("Sorry, there is a problem with the speech service.")
            return None

def jarvis():
    """Main function for Jarvis Assistant."""
    speak("Hello, I am Jarvis. How can I assist you today?")
    while True:
        query = listen()
        if query is None:
            continue

        # Time
        if "time" in query:
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            speak(f"The time is {current_time}")

        # Wikipedia
        elif "wikipedia" in query:
            speak("Searching Wikipedia...")
            query = query.replace("wikipedia", "")
            try:
                result = wikipedia.summary(query, sentences=2)
                speak(f"According to Wikipedia, {result}")
            except wikipedia.exceptions.DisambiguationError:
                speak("There are multiple results for this query. Please be more specific.")
            except wikipedia.exceptions.PageError:
                speak("Sorry, I couldn't find anything on Wikipedia.")

        # Play YouTube
        elif "play" in query or "youtube" in query:
            video = query.replace("play", "").strip()
            speak(f"Playing {video} on YouTube")
            pywhatkit.playonyt(video)

        # Close applications
        elif "close" in query:
            speak("Which application would you like to close?")
            app_name = listen()
            if app_name:
                speak(f"Closing {app_name}")
                os.system(f"taskkill /f /im {app_name}.exe")

        # Exit
        elif "exit" in query or "bye" in query:
            speak("Goodbye! Have a great day!")
            break

        # Default
        else:
            speak("I'm sorry, I can't help with that right now.")

# Run Jarvis
if __name__ == "__main__":
    jarvis()
