#importing libraries
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

#authenticate to IBM cloud
authenticator = IAMAuthenticator(keys.speech_to_text_key)
speech_to_text = SpeechToTextV1(authenticator=authenticator)
speech_to_text.set_service_url('https://api.au-syd.speech-to-text.watson.cloud.ibm.com/instances/3ea75066-a39a-4845-a367-779c32acc4d6')
authenticator2 = IAMAuthenticator(keys.text_to_speech_key)
text_to_speech = TextToSpeechV1(authenticator=authenticator2)
text_to_speech.set_service_url('https://api.au-syd.text-to-speech.watson.cloud.ibm.com/instances/a247d99d-0d59-493d-aded-e4b8f2fcc8a9')

#run_story() function
def run_story():
    sentences = [random.choice(article)+' '+random.choice(noun)+' ' + random.choice(verb)+' '+random.choice(proposition)+ ' '+random.choice(article)+' '+ random.choice(noun)+'.' for line in range(10)]
    sentences = [sentence.capitalize() for sentence in sentences]
    #print story
    print('YOUR RANDOMLY GENERATED STORY \n')
    for sentence in sentences:
        print(sentence, '\n')
    
    
    #read story aloud
    print('NOW LISTEN TO YOUR STORY \n')
    story = ''
    for sentence in sentences:
        story += sentence +' '
    name = random.choice(noun)+'.wav'
    tts(desired_audio_name = name, text_to_speak = story)
    play_audio(file_name = name)
    print('END OF STORY \n')
    
#Utility functions

#1. Text-to-speech function; tts()
def tts(desired_audio_name, text_to_speak):
    with open(desired_audio_name, 'wb') as audio_file:
        audio_file.write(
            text_to_speech.synthesize(
                text_to_speak,
                voice='en-US_AllisonV3Voice',
                accept='audio/wav'        
            ).get_result().content)
        
#2. play audio function; play_audio()
def play_audio(file_name):
    """Use the pydub module (pip install pydub) to play a WAV file."""
    sound = pydub.AudioSegment.from_wav(file_name)
    pydub.playback.play(sound)

#data base of common words by category
article = ['a', 'an', 'the']

noun = ["Actor", "Gold", "Painting", "Advertisement", "Grass", "Parrot",    "Afternoon", "Greece", "Pencil",     "Airport", "Guitar", "Piano",     "Ambulance", "Hair", "Pillow",    "Animal", "Hamburger", "Pizza",    "Answer", "Helicopter", "Planet",    "Apple", "Helmet", "Plastic",     "Army", "Holiday", "Portugal",    "Australia", "Honey", "Potato",    "Balloon", "Horse", "Queen",     "Banana", "Hospital", "Quill",     "Battery", "House", "Rain",     "Beach", "Hydrogen", "Rainbow",    "Beard", "Ice", "Raincoat",    "Bed", "Insect", "Refrigerator",     "Belgium", "Insurance", "Restaurant",    "Boy", "Iron", "River",    "Branch", "Island", "Rocket",    "Breakfast", "Jackal", "Room",     "Brother", "Jelly", "Rose",    "Camera", "Jewellery", "Russia",     "Candle", "Jordan", "Sandwich",    "Car", "Juice", "School",     "Caravan", "Kangaroo", "Scooter",    "Carpet", "King", "Shampoo",     "Cartoon", "Kitchen", "Shoe",    "China", "Kite", "Soccer",
"Church", "Knife", "Spoon",    "Crayon", "Lamp", "Stone",     "Crowd", "Lawyer", "Sugar",    "Daughter", "Leather", "Sweden",     "Death", "Library", "Teacher",  "Denmark", "Lighter", "Telephone",     "Diamond", "Lion", "Television",    "Dinner", "Lizard", "Tent",     "Disease", "Lock", "Thailand",    "Doctor", "London", "Tomato",     "Dog", "Lunch", "Toothbrush",    "Dream", "Machine", "Traffic",     "Dress", "Magazine", "Train",    "Easter", "Magician", "Truck",     "Egg", "Manchester", "Uganda",    "Eggplant", "Market", "Umbrella",     "Egypt", "Match", "Van",     "Elephant", "Microphone", "Vase",     "Energy", "Monkey", "Vegetable",     "Engine", "Morning", "Vulture",     "England", "Motorcycle", "Wall",    "Evening", "Nail", "Whale",     "Eye", "Napkin", "Window",     "Family", "Needle", "Wire",     "Finland", "Nest", "Xylophone",     "Fish", "Nigeria", "Yacht",     "Flag", "Night", "Yak",     "Flower", "Notebook", "Zebra",     "Football", "Ocean", "Zoo",     "Forest", "Oil", "Garden",     "Fountain", "Orange", "Gas",    "France", "Oxygen", "Girl",    "Furniture", "Oyster", "Glass",    "Garage", "Ghost"]

verb = [    "be", "have", "do", "say", "go", "can", "get", "would", "make", "know", "will", "think", "take", "see", "come", "could", "want", "look", "use", "find", "give", "tell", "work", "may", "should", "call", "try", "ask", "need", "feel", "become", "leave", "put", "mean", "keep", "let", "begin", "seem", "help", "talk", "turn", "start", "might", "show", "hear", "play", "run", "move", "like", "live", "believe", "hold", "bring", "happen", "must", "write", "provide", "sit", "stand", "lose", "pay", "meet", "include", "continue", "set", "learn", "change", "lead", "understand", "watch", "follow", "stop", "create", "speak", "read", "allow", "add", "spend", "grow", "open", "walk", "win", "offer", "remember", "love", "consider", "appear", "buy", "wait", "serve", "die", "send", "expect", "build", "stay", "fall", "cut", "reach", "kill", "remain"]

proposition = ["aboard", "about", "above", "across", "after", "against", "along", "amid", "among", "around", "as", "at", "before", "behind", "below",     "beneath", "beside", "between", "beyond", "but", "by", "considering", "despite", "down", "during", "except", "excluding", "following", "for",     "from", "in", "inside", "into", "like", "near", "of", "off", "on", "onto", "outside", "over", "past", "regarding", "since", "than", "though", "to", "toward", "under", "underneath", "until", "up",     "upon", "versus", "with", "within", "without" ]

#invoke run_story();
if __name__ == '__main__':
    run_story()