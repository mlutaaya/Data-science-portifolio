#Loading libraries
import googletrans
from googletrans import Translator #for inter language translation
import speech_recognition as sr #for speech to text
from gtts import gTTS # for text to text
import os

#Obtaining the language from the user
language = input("""What language would you like to learn today? e.g 'chinese (simplified)': """)
language = language.lower()
print()

#Validating the availability of language in google translate
google_lang =  [lang for lang in googletrans.LANGUAGES.values()]
if not (language in google_lang ):
    raise ValueError('Sorry, the selected language is not supported at the moment. Try another language')

#Speech to text in action!!

# initialize the recognizer
r = sr.Recognizer()

with sr.Microphone() as source:
    # read the audio data from the default microphone
    print ("Start recording audio (time limit: 18 sec)")
    audio_data = r.record(source, duration=15)
    print("Recognizing audio...")
    print()
    # convert speech to text
    text = r.recognize_google(audio_data)
    print(f'YOU SAID: {text}')
    print()

print(f'TRANSLATING:  {text} --->> {language} language')
print()

# loading google translator
translator = Translator() 

#translating...
translation = translator.translate(text, dest = language).text
print(f'TRANSLATION: {translation}')
print()

print(f"""Please listen how you say: "{text}" in {language} language""")

# text to speech in action!!
codes = {value: key for key, value in googletrans.LANGUAGES.items()}
code = codes[language]
myobj = gTTS(text= translation, lang=code, slow=False)
myobj.save(f'{language}_version'+".mp3")

os.system("start "+f'{language}_version'+".mp3")

