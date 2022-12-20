#!/usr/bin/env python3

# NOTE: this example requires PyAudio because it uses the Microphone class 
import time
import os 
import subprocess 
import speech_recognition as sr
import itertools 
import getpass 
from pyChatGPT import ChatGPT 
session_token = 'your_session'
api = ChatGPT(session_token)
#import pyttsx3 

import serial 
import socket # Getting the socket to report back to the system on the main processing of robot control tx
import pickle  
import json 
from google_speech import* 
from googletrans import Translator # Google translate  
import os 
import sys
import  wordninja
import difflib #Finding the similarlity of the matching sequence 

#from translate import Translator 
#translator = Translator(to_lang="zh")
#from nanpy import(ArduinoApi,SerialManager)  

#try:
 #  mcucontrol = serial.Serial('/dev/ttyUSB0',115200) 
#except: 
 #  print("Serial error") 
#engine = pyttsx3.init() 
# this is called from the background thread
#try:
translator = Translator(service_urls=['translate.google.com','translate.google.com',])
lang = 'th'
lang2 = 'en'
sox_effects = ('speed',"1.14")
Activate_word = ["translation","Translation","mode","translate","Translate"] #Activate translate mode concern word need more vocabulary 
Direction_translate = ["to","in to"]

#List language of translation function 
Languages = {
    'af': 'Afrikaans',
    'sq': 'Albanian',
    'am': 'Amharic',
    'ar': 'Arabic',
    'hy': 'Armenian',
    'az': 'Azerbaijani',
    'eu': 'Aasque',
    'be': 'Belarusian',
    'bn': 'Bengali',
    'bs': 'Bosnian',
    'bg': 'Bulgarian',
    'ca': 'Batalan',
    'ceb': 'Bebuano',
    'ny': 'Chichewa',
    'zh-cn': 'Chinese',
    'zh-tw': 'Chinese (traditional)',
    'co': 'Corsican',
    'hr': 'Croatian',
    'cs': 'Czech',
    'da': 'Danish',
    'nl': 'Dutch',
    'en': 'English',
    'eo': 'Esperanto',
    'et': 'Estonian',
    'tl': 'Filipino',
    'fi': 'Finnish',
    'fr': 'French',
    'fy': 'Frisian',
    'gl': 'Galician',
    'ka': 'Georgian',
    'de': 'German',
    'el': 'Greek',
    'gu': 'Gujarati',
    'ht': 'Haitian creole',
    'ha': 'Hausa',
    'haw': 'Hawaiian',
    'iw': 'Hebrew',
    'he': 'Hebrew',
    'hi': 'Hindi',
    'hmn': 'Hmong',
    'hu': 'Hungarian',
    'is': 'Icelandic',
    'ig': 'Igbo',
    'id': 'Indonesian',
    'ga': 'Irish',
    'it': 'Italian',
    'ja': 'Japanese',
    'jw': 'Javanese',
    'kn': 'Kannada',

    'kk': 'Kazakh',
    'km': 'Khmer',
    'ko': 'Korean',
    'ku': 'Kurdish (kurmanji)',
    'ky': 'Kyrgyz',
    'lo': 'Lao',
    'la': 'Latin',
    'lv': 'Latvian',
    'lt': 'Lithuanian',
    'lb': 'Luxembourgish',
    'mk': 'Macedonian',
    'mg': 'Malagasy',
    'ms': 'Malay',
    'ml': 'Malayalam',
    'mt': 'Maltese',
    'mi': 'Maori',
    'mr': 'Marathi',
    'mn': 'Mongolian',
    'my': 'Myanmar (burmese)',
    'ne': 'Nepali',
    'no': 'Norwegian',
    'or': 'Odia',
    'ps': 'Pashto',
    'fa': 'Persian',
    'pl': 'Polish',
    'pt': 'Portuguese',
    'pa': 'Punjabi',
    'ro': 'Romanian',
    'ru': 'Russian',
    'sm': 'Samoan',
    'gd': 'Scots gaelic',
    'sr': 'Serbian',
    'st': 'Sesotho',
    'sn': 'Shona',
    'sd': 'Sindhi',
    'si': 'Sinhala',
    'sk': 'Slovak',
    'sl': 'Slovenian',
    'so': 'Somali',
    'es': 'Spanish',
    'su': 'Sundanese',
    'sw': 'Swahili',
    'sv': 'Swedish',
    'tg': 'Tajik',
    'ta': 'Tamil',
    'te': 'Telugu',
    'th': 'Thai',
    'tr': 'Turkish',
    'uk': 'Ukrainian',
    'ur': 'Urdu',
    'ug': 'Uyghur',
    'uz': 'Uzbek',
    'vi': 'Vietnamese',
    'cy': 'Welsh',
    'xh': 'Xhosa',
    'yi': 'Yiddish',
    'yo': 'Yoruba',
    'zu': 'Zulu'}
#Data of preposition word in the list of the dictionary file 

Detected_language = ['th','en'] #Detected language   
Inner_trans = 'en'
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
address = "127.0.0.1"  
user = getpass.getuser() # Get user 
PATH_SR = "/home/"+user+"/Bot_listener/"

def UDP_text_sender(send_text): 
        try:
           send_speech_data = {send_text:Detected_language[0]}
           jsondata = json.dumps(send_speech_data) 
           message = pickle.dumps(jsondata) 
           sock.sendto(message,(address,5040))  
        except: 
            reboot = subprocess.check_output("python3 "+PATH_SR+"listening.py")

def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3 
 #Function call back of the speech recognition command        
def callback(recognizer, audio):
    # received audio data, now we'll recognize it using Google Speech Recognition
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        #sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        #address = "127.0.0.1"  
        print("Speech Recognition thinks you said " + recognizer.recognize_google(audio,language = 'th')) # Setting the default language from the json file 
        send_speech_data = {recognizer.recognize_google(audio,language = 'th'):Detected_language[0]}  
        jsondata = json.dumps(send_speech_data) 
        message = pickle.dumps(jsondata) 
        sock.sendto(message,(address,5040))  
        
        '''
        translation = translator.translate(recognizer.recognize_google(audio,language = 'th'))
        print(translation)
        speech = Speech(translation,lang)
        speech.play(sox_effects)
        '''
        if len(Detected_language) >=2:
           try:
              translations = translator.translate(str(recognizer.recognize_google(audio,language =str(Detected_language[0]))),dest =str(Detected_language[len(Detected_language)-1]))
              translations2 = translator.translate(str(recognizer.recognize_google(audio,language =str(Detected_language[0]))),dest = Inner_trans)
           except: 
               print("Error in language translation mode sending request reboot process")
               reboot = subprocess.check_output("python3 "+PATH_SR+"listening.py") 
        #Setting default of the language detected from the function of the language detection activate from the unknown non destination language 
        if len(Detected_language) <2:
            try:
               translations = translator.translate(str(recognizer.recognize_google(audio,language =str(Detected_language[0]))),dest =str(Detected_language[0]))
               translations2 = translator.translate(str(recognizer.recognize_google(audio,language =str(Detected_language[0]))),dest = Inner_trans)
            except: 
               print("Error in language translation mode sending")
               #reboot = subprocess.check_output("python3 "+PATH_SR+"listening.py")
        #for translation in translations:translations.text
        print(translations.text) # Print out translation
        #UDP_text_sender(translations.text)
        if len(Detected_language) >=2: 
           try:  
               speech = Speech(translations.text,Detected_language[1])
           except: 
               print("Speech recognition alert fail")
               #reboot = subprocess.check_output("python3 "+PATH_SR+"listening.py")
        if len(Detected_language) <2 and Detected_language !=[]: 
            try: 
               speech = Speech(translations.text,Detected_language[0]) 
               Detected_language.clear()
               Detected_language.append('en')
               speech = Speech("Not detected destination language now using"+"\t"+str(Languages.get(Detected_language[0])+"\t"+"as default"),'en')
            except: 
                print("Not detected language in the list ")
                #reboot = subprocess.check_output("python3 "+PATH_SR+"listening.py")
        resp = api.send_message(str(translations2.text)).get('message')
        speech = Speech(translator.translate(resp,dest ='th').text,'th')
        speech.play(sox_effects)
        splitword = wordninja.split(resp) #str(translations2.text)
        print(splitword)
        word_intersection = intersection(splitword,Activate_word)
        print("Getting the intersection word",word_intersection) 
        superposition = intersection(word_intersection,Activate_word)
        print("Word superpositioning",superposition)
        percent=difflib.SequenceMatcher(None,superposition,Activate_word)
        print(percent.ratio()*100)
        values_languages = list(Languages.values())
        key_languages = list(Languages.keys()) 
        print(values_languages)
        if percent.ratio()*100 >= 33:
                  print("Detect translation mode")
                  print(values_languages)
                  Detected_language.clear() 
                  for lang in range(0,len(splitword)):
                           if splitword[lang] in values_languages:
                                     Detected_language.append(key_languages[values_languages.index(splitword[lang])]) # Detected language translation on each language detected in the array 
                  print(Detected_language)
         
        #speech.play(sox_effects)

    except sr.UnknownValueError:
        print("Speech Recognition could not understand audio")
        #reboot = subprocess.check_output("python3 "+PATH_SR+"listening.py")
    except sr.RequestError as e:
        print("Could not request results from Catbot Speech Recognition service; {0}".format(e))
        reboot = subprocess.check_output("python3 "+PATH_SR+"listening.py")        

r = sr.Recognizer()
m = sr.Microphone()
with m as source:
    r.adjust_for_ambient_noise(source)  # we only need to calibrate once, before we start listening


# start listening in the background (note that we don't have to do this inside a `with` statement)
stop_listening = r.listen_in_background(m, callback)
# `stop_listening` is now a function that, when called, stops background listening

# do some unrelated computations for 5 seconds
for i in itertools.count():time.sleep(0.01)  # we're still listening even though the main thread is doing other things

# calling this function requests that the background listener stop listening
#stop_listening(wait_for_stop=False)

# do some more unrelated things
#whil True:time.sleep(0.1) # we're not listening anymore, even though the background thread might still be running for a second or two while cleaning up and stopping
#raise SystemExit


