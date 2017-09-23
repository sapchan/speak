

# NOTE: this example requires PyAudio because it uses the Microphone class

import speech_recognition as sr

# obtain path to "english.wav" in the same folder as this script
from os import path
AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "english.wav")
#AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "computer_two_hours.wav")
#AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "egotistical.wav")
#AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "hawking01.wav")

# AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "french.aiff")
# AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "chinese.flac")

# use the audio file as the audio source
r = sr.Recognizer()
with sr.AudioFile(AUDIO_FILE) as source:
    audio = r.record(source) # read the entire audio file

words_arr = "wordies"

# recognize speech using Sphinx
try:
    words_arr = r.recognize_sphinx(audio)
    print("Sphinx thinks you said " + words_arr)

except sr.UnknownValueError:
    print("Sphinx could not understand audio")
except sr.RequestError as e:
    print("Sphinx error; {0}".format(e))


# recognize speech using Google Speech Recognition
try:
    # for testing purposes, we're just using the default API key
    # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
    # instead of `r.recognize_google(audio)`
    print("Google Speech Recognition thinks you said " + r.recognize_google(audio))
except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))


print("Final: " + words_arr)
