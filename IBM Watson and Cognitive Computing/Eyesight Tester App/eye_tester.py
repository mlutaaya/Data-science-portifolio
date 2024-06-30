import keys
import re
import time
import json
import ffmpeg
from ibm_watson import SpeechToTextV1
from ibm_watson.websocket import RecognizeCallback, AudioSource
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import TextToSpeechV1
import speech_recognition as sr
import pyaudio
import pydub
import pydub.playback
import wave
from textblob import TextBlob
import random
import string
from IPython.display import display, Markdown
import numpy as np

#list of alphabets--> used in generating random names
alphabets = string.ascii_lowercase

#authenticate to IBM cloud
authenticator = IAMAuthenticator(keys.speech_to_text_key)
speech_to_text = SpeechToTextV1(authenticator=authenticator)
speech_to_text.set_service_url('https://api.au-syd.speech-to-text.watson.cloud.ibm.com/instances/3ea75066-a39a-4845-a367-779c32acc4d6')
authenticator2 = IAMAuthenticator(keys.text_to_speech_key)
text_to_speech = TextToSpeechV1(authenticator=authenticator2)
text_to_speech.set_service_url('https://api.au-syd.text-to-speech.watson.cloud.ibm.com/instances/a247d99d-0d59-493d-aded-e4b8f2fcc8a9')


# run eye test function; run_eye_test();\
def run_eye_test():
    #randomizing eye selection and task to be completed.
    eyes = random.choices(['left', 'right'], k = 3)
    tasks = [str(x) for x in random.sample(range(1,12), k = 3)]
    
    #obtaining responses from 3 tasks
    responses = []
    for idx in range(3):
        input(f'Close your {eyes[idx]} eye and press ENTER') 
        print()
        print(f'TASK {idx}:')
        print()
        x = tasks[idx]
        show_me(text = snellen_chart[x][0], font_size = snellen_chart[x][1])
        print('Please read aloud the letters shown')
        print()
        response = stt_super()
        responses.append(response)
        print()
    #Assessing response.
    Actuals = [snellen_chart[actual][0] for actual in tasks]
    Actuals = np.array([word.lower() for word in Actuals])
    scores = [snellen_chart[actual][2] for actual in tasks]
    responses = np.array(responses)
    results = Actuals == responses
    print()
    print('EYE TEST RESULTS:')
    print()
    for index, result in enumerate(results):
        if result == True:
            speak = str(f'* TASK {index} was level {tasks[index]} on the Snellen Chart and your score on this task is {scores[index]}')
            print(speak)
            nm =  ''.join(random.choices(alphabets, k=5))+".wav"
            tts(desired_audio_name = nm, text_to_speak = speak)
            print('- Results in Audio', f'{0x1F50A:c}')
            play_audio(nm)
            print()
        else:
            speak2 = str(f'* TASK {index} was level {tasks[index]} on the Snellen Chart and we are sorry to inform you that you did not pass the task')
            print(speak2)
            nm2 = ''.join(random.choices(alphabets, k=5))+".wav"
            tts(desired_audio_name = nm2, text_to_speak = speak2)
            print('- Results in Audio', f'{0x1F50A:c}')
            play_audio(nm2)
            print()
    
#Snellen charts
snellen_chart = {
    '1': ['E', 152, '20/200'],
    '2': ['F P', 130, '20/100'],
    '3': ['T O Z',  108, '20/70'],
    '4': ['L P E D', 87, '20/50'],
    '5': ['P E C F D', 65, '20/40'],
    '6': ['E D F C Z P', 43, '20/30'],
    '7': ['F E L O P Z D', 33, '20/25'],
    '8': ['D E F P O T E C', 21, '20/20'],
    '9': ['L E F O D P C T', 15, '20/15'],
    '10':['F D P L T C E 0', 9, '20/13'],
    '11':['P E Z O L C F T D', 3, '20/10']
}

#Utility functions

#1.google's speech to text
def stt_super():
    # initialize the recognizer
    r = sr.Recognizer()
    
    with sr.Microphone() as source:
        # read the audio data from the default microphone
        print ("Start recording audio (time limit: 15sec)", f'{0x1F399:c}')
        audio_data = r.record(source, duration=15)
        print("Recognizing audio", f'{0x1F504:c}')
        print()
        # convert speech to text
        text = r.recognize_google(audio_data)
        print('Recording done', f'{0x2705:c}')
        return(text)

#2. Text-to-speech function; tts()
def tts(desired_audio_name, text_to_speak):
    with open(desired_audio_name, 'wb') as audio_file:
        audio_file.write(
            text_to_speech.synthesize(
                text_to_speak,
                voice='en-US_AllisonV3Voice',
                accept='audio/wav'        
            ).get_result().content)
        
#3. play audio function; play_audio()
def play_audio(file_name):
    """Use the pydub module (pip install pydub) to play a WAV file."""
    sound = pydub.AudioSegment.from_wav(file_name)
    pydub.playback.play(sound)


#display letters function; show_me();
def show_me(text, font_size):
    markdown_content = f"<span style='font-size:{font_size}px'>{text:^}</span>"
    display(Markdown(markdown_content))

#invoke run_eye_test();
if __name__ == '__main__':
    run_eye_test()