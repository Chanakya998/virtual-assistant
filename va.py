'''from gtts import gTTS
speech = gTTS("Hello Good Evening Chanakya Varma, How are you")
print(speech)
a=speech.save("audio.mp3")'''
from gtts import gTTS
import speech_recognition as sr
from time import ctime,sleep
import re
import playsound
import uuid
import os
import smtplib
import webbrowser

#function to make it listen
def listen():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        print("Start Speaking...")
        audio=r.listen(source,phrase_time_limit=5)
    data=""
    #Exception handling
    try:
        data=r.recognize_google(audio,language='en-US')
        print("You said ",data)
    except sr.UnknownValueError:
        print("I am unable to hear you")
    except sr.RequestError as e:
        print("Request Failed")
    return data
#listen()
#function to make virtual assistant to speak
def respond(String):
    print(String)
    tts = gTTS(text = String,lang = 'en-US')
    tts.save("speech.mp3")
    filename = "Speech%s.mp3"%str(uuid.uuid4())
    tts.save(filename)
    playsound.playsound(filename)
    os.remove(filename)

#Virtual Assistant actions
def virtual_assistant(data):
    """give your actions"""
    if "how are you" in data:
        listening = True
        respond("Good and doing well")

    if "weather" in data:
        listening = True
        respond("Sorry, I'm still working on it")

    if "time" in data:
        listening = True
        respond(ctime())

    if "open google" in data.casefold():
        listening = True
        reg_ex = re.search('open google(.*)',data)
        url = "https://www.google.com/"
        if reg_ex:
            sub = reg_ex.group(1)
            url = url + 'r/'
        webbrowser.open(url)
        respond("Success")

    if "email" in data:
        listening = True
        respond("Whom should i send email to?")
        to = listen()
        edict = {'Chanakya':'cvbhallam15@gmail.com','sam':'email@gmail.com'}
        toaddr = edict[to]
        respond("What is the Subject?")
        subject = listen()
        respond("What should i tell that person?")
        message = listen()
        content = 'Subject :{}\n\n{}'.format(subject,message)

        #init gmail SMTP
        mail = smtplib.SMTP('smtp.gmail.com',587)
        #identify the server
        mail.ehlo()
        mail.starttls()
        #login
        mail.login('email@gmail.com','password') #enter mailid and password make sure you enable less secure app access
        mail.sendmail('email@gmail.com',toaddr,content)
        mail.close()
        respond('Email Sent')
        
    if "locate" in data:
        webbrowser.open('https://www.google.com/maps/search/'+data.replace("locate",""))
        result = "Located"
        respond("Located {}".format(data.replace("locate","")))
    if "video" in data:
        webbrowser.open("https://www.youtube.com/results?search_query="+data.replace("video",""))
        result = "Success"
        respond("Shown video {}".format(data.replace("video","")))

    if "stop" in data:
        listening=False
        print("Stopped Listening")
        respond("Okay done... See you soon : ) ")

    try:
        return listening
    except UnboundLocalError:
        print("Timedout")

respond("Hey Chanakya how can I help you")
listening = True
while listening ==True:
    data = listen()
    listening = virtual_assistant(data)