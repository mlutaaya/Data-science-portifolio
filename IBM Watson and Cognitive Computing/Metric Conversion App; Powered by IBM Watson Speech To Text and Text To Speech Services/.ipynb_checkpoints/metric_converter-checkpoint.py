#importing the required libraries
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
from unitpy import U, Q , Unit, Quantity
from quantities import units as u
from textblob import TextBlob
import random
import string

#list of alphabets--> used in generating random names
alphabets = string.ascii_lowercase

#authenticate to IBM cloud
authenticator = IAMAuthenticator(keys.speech_to_text_key)
speech_to_text = SpeechToTextV1(authenticator=authenticator)
speech_to_text.set_service_url('https://api.au-syd.speech-to-text.watson.cloud.ibm.com/instances/3ea75066-a39a-4845-a367-779c32acc4d6')
authenticator2 = IAMAuthenticator(keys.text_to_speech_key)
text_to_speech = TextToSpeechV1(authenticator=authenticator2)
text_to_speech.set_service_url('https://api.au-syd.text-to-speech.watson.cloud.ibm.com/instances/a247d99d-0d59-493d-aded-e4b8f2fcc8a9')

#the run_metric converter function
def run_metric_converter():
    #Prompt the user to ask a metric conversion.
    input("""Press 'Enter' then ask your metric conversion""")
    
    #Record the question & Transcribe the question to text.
    transcription = stt_super()

    #print text
    print()
    print(f'YOU WANT TO KNOW: {transcription}?')
    print()
    print('Just a moment...')
    print()

    # steps 4 to 8 as detailed in the notebook
    preprocess(text =  transcription)

#Utility functions.

#1. Speech-to-text function; stt()
def stt(audio_file_name):
    class MyRecognizeCallback(RecognizeCallback):
        def __init__(self):
            super().__init__()
            self.transcriptions = []
    
        def on_data(self, data):
            if 'results' in data:
                for result in data['results']:
                    if result['final']:
                        self.transcriptions.append(result['alternatives'][0]['transcript'])
    
        def on_error(self, error):
            print('Error received: {}'.format(error))
    
        def on_inactivity_timeout(self, error):
            print('Inactivity timeout: {}'.format(error))
    
        def get_transcription(self):
            return ' '.join(self.transcriptions)
            
    myRecognizeCallback = MyRecognizeCallback()
    
    with open(audio_file_name, 'rb') as audio_file:
        audio_source = AudioSource(audio_file)
        speech_to_text.recognize_using_websocket(
            audio=audio_source,
            content_type='audio/wav',
            recognize_callback=myRecognizeCallback,
            model='en-US_BroadbandModel'
        )
    
    # Wait for the transcription process to complete
    time.sleep(15)  
    
    final_transcription = myRecognizeCallback.get_transcription()
    return final_transcription
    
#2. Text-to-speech function; tts()
def tts(desired_audio_name, text_to_speak):
    with open(desired_audio_name, 'wb') as audio_file:
        audio_file.write(
            text_to_speech.synthesize(
                text_to_speak,
                voice='en-US_AllisonV3Voice',
                accept='audio/wav'        
            ).get_result().content)
        
#3. Record audio function; record_now()
def record_now(file_name):
    FRAME_RATE = 44100  # number of frames per second
    CHUNK = 1024  # number of frames read at a time
    FORMAT = pyaudio.paInt16  # each frame is a 16-bit (2-byte) integer
    CHANNELS = 2  # 2 samples per frame
    SECONDS = 10  # total recording time
 
    recorder = pyaudio.PyAudio()  # opens/closes audio streams

    # configure and open audio stream for recording (input=True)
    audio_stream = recorder.open(format=FORMAT, channels=CHANNELS, 
        rate=FRAME_RATE, input=True, frames_per_buffer=CHUNK)
    audio_frames = []  # stores raw bytes of mic input
    print('Recording 10 seconds of audio')

    # read 5 seconds of audio in CHUNK-sized pieces
    for i in range(0, int(FRAME_RATE * SECONDS / CHUNK)):
        audio_frames.append(audio_stream.read(CHUNK))

    print('Recording complete')
    audio_stream.stop_stream()  # stop recording
    audio_stream.close()  
    recorder.terminate()  # release underlying resources used by PyAudio

    # save audio_frames to a WAV file
    with wave.open(file_name, 'wb') as output_file:
        output_file.setnchannels(CHANNELS)
        output_file.setsampwidth(recorder.get_sample_size(FORMAT))
        output_file.setframerate(FRAME_RATE)
        output_file.writeframes(b''.join(audio_frames))

#4. play audio function; play_audio()
def play_audio(file_name):
    """Use the pydub module (pip install pydub) to play a WAV file."""
    sound = pydub.AudioSegment.from_wav(file_name)
    pydub.playback.play(sound)
    
#5. actual conversion function: preprocess()
def preprocess(text):
    #extracting units and digits from the transcribed speech to text
    unit_symbols = [foo.symbol for _, foo in u.__dict__.items() if isinstance(foo, type(u.m))]
    unit_names = [bar for bar, foo in u.__dict__.items() if isinstance(foo, type(u.m))]
    units = []
    digit = float(re.findall(r'\d+', text)[0])
    text = text.lower()
    words  = TextBlob(text).words.singularize()
    
    source = words[2]
    destination = words[4]
    
    #performing conversion.
    try:
        #perform conversion
        q = digit * U(source)
        conversion = float(re.findall(r'\d+\.\d{3}', str(q.to(destination)))[0])
        solution =  str('There are' + ' '+ str(conversion) + ' ' + (destination if len(destination.pluralize()) == len(destination) +1 else destination.pluralize()) + ' '+ 'in' + ' ' + str(digit) + ' ' + (source if len(source.pluralize()) == len(source) +1 else source.pluralize()))
        random_name = ''.join(random.choices(alphabets, k=5))+'.wav'
        tts(desired_audio_name = random_name, text_to_speak = solution)
        print('Listen to your answer', f'{0x1F50A:c}')
        print()
        play_audio(random_name)
        print('ANSWER:', solution, f"{0x1F609:c}")
        
    except ValueError:
        #raise error message 
        speak = 'That is an invalid conversion.'
        random_name2 = ''.join(random.choices(alphabets, k=5))+'.wav'
        tts(desired_audio_name = random_name2, text_to_speak = speak)
        print('Listen to error noted', f'{0x1F50A:c}')
        print()
        play_audio(random_name2)
        print(speak, f'{0x1F61E:c}')

#google's speech to text
def stt_super():
    # initialize the recognizer
    r = sr.Recognizer()
    
    with sr.Microphone() as source:
        # read the audio data from the default microphone
        print ("Start recording audio (time limit: 10sec)", f'{0x1F399:c}')
        audio_data = r.record(source, duration=10)
        print("Recognizing audio", f'{0x1F504:c}')
        print()
        # convert speech to text
        text = r.recognize_google(audio_data)
        print('Recording done', f'{0x2705:c}')
        return(text)
        
#Invoking the run_metric_converter() function
if __name__ == '__main__':
    run_metric_converter()