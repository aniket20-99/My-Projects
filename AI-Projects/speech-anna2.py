import speech_recognition as sr
import pyttsx3 as pt
import pywhatkit as pk
import sys

# Initialize recognizer and TTS engine
listening = sr.Recognizer()
engine = pt.init()

# Function to speak
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Noise-cancelled listening
def get_audio_noise_cancelled():
    cmd = ""
    try:
        with sr.Microphone() as mic:
            # Adjust for ambient noise (background)
            listening.adjust_for_ambient_noise(mic, duration=1)
            print("Listening (noise-cancelled)...")
            voice = listening.listen(mic)
            cmd = listening.recognize_google(voice)
            cmd = cmd.lower()

            if 'anna' in cmd:  # Only respond if "Anna" is said
                cmd = cmd.replace('anna', '').strip()
                print("Command:", cmd)
    except sr.UnknownValueError:
        print("I didn't catch that.")
    except sr.RequestError:
        print("Service error.")
    return cmd

# Main function
def run_anna():
    while True:
        cmd = get_audio_noise_cancelled()
        if cmd == "":
            continue  # ignore empty inputs

        # Play song command
        if 'play' in cmd:
            song = cmd.replace('play', '').strip()
            speak("Playing " + song)
            pk.playonyt(song)

        # Quit/exit command (immediate quit)
        elif 'quit' in cmd or 'exit' in cmd or 'ok bye anna' in cmd:
            speak("Goodbye sir, see you later")
            sys.exit()  # exits the program immediately

# Run Anna
run_anna()
