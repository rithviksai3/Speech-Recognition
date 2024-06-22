from django.shortcuts import render
import speech_recognition as sr
from AppOpener import open
import win32com.client
import webbrowser
from django.contrib import messages
import pythoncom
# Create your views here.
def index(request):
    if request.method=='POST':
        speaker=win32com.client.Dispatch('SAPI.SpVoice',pythoncom.CoInitialize())
        speaker.Speak("welcome back")
        speaker.Speak("start speaking and say quit when completed")
        c=1
        speak=True
        while speak:
            f=0
            r=sr.Recognizer()
            with sr.Microphone() as source:
                r.pause_threshold=1
                audio=r.listen(source)
                try:
                    print("trying")
                    query=r.recognize_google(audio,language="en-in")
                    text=query
                except:
                    f=2
                    text="repeat again"
            if "quit" in text.lower():
                f=2
                speak=False
            if "show me what i say" in text.lower():
                f=1
                speaker.Speak("ok")
            if "good morning" in text.lower():
                f=1
                speaker.Speak("good morning rithvik")
            if "open camera" in text.lower():
                f=1
                speaker.Speak("opening camera")
                open("camera")
            sites=[["google","https://www.google.com"],["youtube","https://www.youtube.com"],["wikipedia","https://www.wikipesdia.com"]]
            for site in sites:
                if f"open {site[0]}".lower() in text.lower():
                    f=1
                    speaker.Speak(f"opening {site[0]}")
                    webbrowser.open(site[1])
            if f==0: 
                speaker.Speak(text)
                messages.error(request,f'{c}:{text}')
                c=c+1
            elif f==2:
                speaker.Speak(text)
    return render(request,'index.html')