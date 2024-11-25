#Yara is a voice-activated virtual assistant designed to perform tasks such as web
#browsing, playing music, fetching news, and responding to user queries using OpenAI's GPT-3.5-turbo model.

# Import necessary libraries
import speech_recognition as sr  # For recognizing speech
import webbrowser  # For opening websites in a browser
import pyttsx3  # For text-to-speech functionality
import musicLibrary  # Presumably your custom library for music URLs
import requests  # For making HTTP requests (e.g., fetching news)
from openai import OpenAI  # OpenAI's library for GPT-3 (or GPT-4)
from gtts import gTTS  # For text-to-speech using Google TTS
import pygame  # For playing audio files
import os  # For file operations like deleting temporary files


# Initialize the speech recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()  # For text-to-speech using pyttsx3
newsapi = "4e90860e101947c4bfe44fda4e7667b4"  # Insert your NewsAPI key here

# Function to speak text using pyttsx3 (older method)
def speak_old(text):
    engine.say(text)  # Convert text to speech
    engine.runAndWait()  # Wait until speaking is done

# Function to speak text using gTTS (Google Text-to-Speech)
def speak(text):
    # Convert the text to speech using gTTS and save it as an MP3 file
    tts = gTTS(text)
    tts.save('temp.mp3')  # Save the audio to a temporary MP3 file

    # Initialize Pygame mixer for audio playback
    pygame.mixer.init()

    # Load the generated MP3 file into the mixer
    pygame.mixer.music.load('temp.mp3')

    # Play the audio
    pygame.mixer.music.play()

    # Keep the program running until the audio finishes playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)  # Ensure the program waits while audio is playing

    # Unload the music and delete the temporary MP3 file
    pygame.mixer.music.unload()
    os.remove("temp.mp3")  # Clean up by removing the temp file

# Function to process commands using OpenAI's API (GPT-3 or GPT-4)
def aiProcess(command):
    # Initialize OpenAI client with your API key
    client = OpenAI(api_key="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")

    # Send the command to OpenAI for processing and get the response
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",  # Choose the model
        messages=[  # Conversation history with system and user messages
            {"role": "system", "content": "You are a virtual assistant named Yara skilled in general tasks like Alexa and Google Cloud. Give short responses please"},
            {"role": "user", "content": command}
        ]
    )

    # Return the AI's response (the assistant's reply)
    return completion.choices[0].message.content

# Function to process different voice commands
def processCommand(c):
    # Check if the command is to open a website
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    
    # Check if the command is to play a song from the music library
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]  # Extract song name after "play"
        link = musicLibrary.music[song]  # Get the song link from the music library
        webbrowser.open(link)  # Open the song link in the browser

    # Check if the command is related to getting news
    elif "news" in c.lower():
        # Make a GET request to the NewsAPI to fetch top headlines
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
        if r.status_code == 200:  # If the request was successful
            # Parse the JSON response
            data = r.json()
            
            # Extract the list of articles from the response
            articles = data.get('articles', [])
            
            # Iterate through the articles and read out the headlines
            for article in articles:
                speak(article['title'])  # Speak out each headline

    elif "stop the program" in c.lower():
        speak("Okay, stopping the program. Goodbye!")
        exit()  # Exit the program gracefully

    # If the command doesn't match any predefined ones, pass it to OpenAI for processing
    else:
        output = aiProcess(c)  # Get a response from the AI
        speak(output)  # Speak the AI's response

# Main execution block
if __name__ == "__main__":
    speak("Initializing Yaara....")  # Speak when the program starts

    while True:
        # Continuously listen for the wake word "Yara"
        r = sr.Recognizer()
         
        print("recognizing...")
        try:
            # Capture audio from the microphone
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source, timeout=5, phrase_time_limit=10)  # Listen for 2 seconds
                # Waits up to 5 seconds for the user to start speaking.
                #phrase_time_limit=10: Allows the user to speak for up to 10 seconds.
            word = r.recognize_google(audio)  # Recognize the speech using Google's API
            
            # Check if the wake word "Yara" was said
            if word.lower() == "yara" or word.lower() == "yaara" or word.lower() =="yaarra":
                speak("Yaa")  # Confirm that Yara is listening
                # Now listen for the actual command
                with sr.Microphone() as source:
                    print("Yaara Active...")  # Indicate Yara is active
                    audio = r.listen(source)  # Listen for the command
                    command = r.recognize_google(audio)  # Convert the command to text

                    processCommand(command)  # Process the command

        except Exception as e:
            # If there's an error (e.g., no audio detected), print it
            print("Error: {0}".format(e))
