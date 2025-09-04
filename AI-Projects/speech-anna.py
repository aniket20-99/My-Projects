import speech_recognition as sr
import pyttsx3 as pt
import pywhatkit as pk

listening = sr.Recognizer()
engine = pt.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def get_audio():
    try:
        with sr.Microphone() as mic:
            print('Listenning...')
            voice = listening.listen(mic)
            cmd = listening.recognize_google(voice)
            cmd = cmd.lower()
            
            if 'anna' in cmd:
                cmd = cmd.replace('anna', '')
                print(cmd)
    except:
        pass
    return cmd

def run_anna():
    cmd = get_audio()
    print(cmd)    
    
    if 'play' in cmd:
        song = cmd.replace('play', '')           
        speak('playing...' + song)
        pk.playonyt(song)
    
run_anna()