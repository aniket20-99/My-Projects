import speech_recognition as sr
import pyttsx3 as pt
import pywhatkit as pk
import sys
import pyautogui
import time

# Initialize recognizer and TTS engine
listening = sr.Recognizer()
engine = pt.init()

# Select an expressive female voice
voices = engine.getProperty('voices')
for voice in voices:
       if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
        engine.setProperty('voice', voice.id)
        break

engine.setProperty('rate', 125)    # speaking speed
engine.setProperty('volume', 1.0)  # max volume
try:
    engine.setProperty('pitch', 120)  # warmer tone
except Exception:
    pass

# Function to speak
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Noise-cancelled listening
def get_audio_noise_cancelled(timeout=None):
    cmd = ""
    try:
        with sr.Microphone() as mic:
            listening.adjust_for_ambient_noise(mic, duration=1)
            if timeout:
                print(f"Listening (noise-cancelled, {timeout}s timeout)...")
                voice = listening.listen(mic, timeout=timeout)
            else:
                print("Listening (noise-cancelled)...")
                voice = listening.listen(mic)
            cmd = listening.recognize_google(voice)
            cmd = cmd.lower()
            if 'anna' in cmd:
                cmd = cmd.replace('anna', '').strip()
                print("Command:", cmd)
    except sr.WaitTimeoutError:
        print("No response detected within timeout.")
    except sr.UnknownValueError:
        print("I didn't catch that.")
    except sr.RequestError:
        print("Service error.")
    return cmd

# Main function
def run_anna():
    # Greeting
    speak("Hi! sir, Anna here. How are you ?")

    # Listen to initial response with 10-second timeout
    response = get_audio_noise_cancelled(timeout=10)
    if response:
        print("User said:", response)
        speak("How can I help you, sir?")
    else:
        speak("I didn't hear anything. Goodbye!")
        sys.exit()
    
    # Main loop for commands (normal listening, no timeout)
    while True:
        cmd = get_audio_noise_cancelled()  # normal listening
        if cmd == "":
            continue

        # Play a song
        if 'play' in cmd:
            song = cmd.replace('play', '').strip()
            speak("Playing " + song)
            pk.playonyt(song)
            time.sleep(10)  # wait for YouTube to load

        # Next song
        elif 'next' in cmd:
            speak("Skipping to next song")
            pyautogui.hotkey('shift', 'n')  # affects currently active tab only

        elif 'previous song' in cmd:
            speak("Skipping to previous song")
            pyautogui.hotkey('shift', 'p') 

        # Pause/Resume
        elif 'pause' in cmd or 'stop song' in cmd:
            speak("Pausing the song")
            pyautogui.press('space')  # active tab only

        elif 'resume' in cmd or 'play song' in cmd:
            speak("Resuming the song")
            pyautogui.press('space')  # active tab only

        # Volume control
        elif 'volume up' in cmd:
            speak("Increasing volume")
            pyautogui.press('up')  # active tab only

        elif 'volume down' in cmd:
            speak("Decreasing volume")
            pyautogui.press('down')  # active tab only

        # Quit
        elif 'quit' in cmd or 'exit' in cmd or 'ok bye anna' in cmd:
            speak("Goodbye sir, see you later")
            sys.exit()

# Run Anna
run_anna()
