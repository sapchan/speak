# MHacks X
# Speak - Speech Recognition

import contextlib
import wave
from os import path
import speech_recognition as sr
from textblob import TextBlob
from watson_developer_cloud import NaturalLanguageUnderstandingV1
import watson_developer_cloud.natural_language_understanding.features.v1 \
    as Features
import json

from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool


FILLER_WORDS = ["ah", "um", "uh", "so", "and", "oh", "like", "you know", "I mean"]
# AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "computer_two_hours.wav")
# AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "egotistical.wav")
# AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "hawking01.wav")
BLUEMIX_USERNAME = ""
BLUEMIX_PASSWORD = ""
BLUEMIX_API_VERSION = "2017-02-27"

with open('mhacksx-credentials.json') as data_file:
    data = json.load(data_file)
    BLUEMIX_USERNAME = data['username']
    BLUEMIX_PASSWORD = data['password']

natural_language_understanding = NaturalLanguageUnderstandingV1(username=BLUEMIX_USERNAME,
                                                                password=BLUEMIX_PASSWORD,
                                                                version=BLUEMIX_API_VERSION)
r = sr.Recognizer()


def acquire_audio(fileName):
    AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), fileName)
    with sr.AudioFile(AUDIO_FILE) as source:
        return r.record(source)  # read the entire audio file


def google_speech_extract_text(audio):
    # recognize speech using Google Speech Recognition
    try:
        return r.recognize_google(audio)
    except sr.UnknownValueError:
        return "Google Speech Recognition could not understand audio"
    except sr.RequestError as e:
        return "Google Speech Error error; {0}".format(e)


def sphinx_extract_text(audio):
    # recognize speech using Sphinx
    try:
        return r.recognize_sphinx(audio)
    except sr.UnknownValueError:
        return "Sphinx could not understand audio"
    except sr.RequestError as e:
        return "Sphinx error; {0}".format(e)


def filler_word_percentage(words_arr, filler_words):
    filler_count = 0
    for filler in filler_words:
        filler_count = filler_count + words_arr.count(filler)
    return (float(filler_count) / len(words_arr)) * 100


def audio_duration(name):
    with contextlib.closing(wave.open(name, 'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)
        return duration  # in seconds


def words_per_minute(word_arr):
    word_count = len(word_arr)
    return (float(word_count) / 15) * 60


def duplicate_word_percentage(words_arr):
    words_as_set = set(words_arr)
    duplicates = len(words_arr) - len(words_as_set)
    duplicate_percent = (float(duplicates) / len(words_arr)) * 100
    return duplicate_percent



def get_json_analysis_results(fileName):
    audio = acquire_audio(fileName)
    words = google_speech_extract_text(audio)
    print("Input: " + fileName)
    print("Output: " + words)
    # print("Google: " + google_speech_extract_text(audio))
    words_arr = words.split(" ")
    # print(len(words_arr))
    # Internet connected calculations
    response = natural_language_understanding.analyze(
        text=words,
        features=[
            Features.Entities(
                emotion=True,
                sentiment=True,
                limit=5
            ),
            Features.Keywords(
                emotion=True,
                sentiment=True,
                limit=5
            )
        ]
    )
    print(json.dumps(response, 2))
    # Local calculations
    print("Filler word percent: " + str(filler_word_percentage(words_arr, FILLER_WORDS)) + "%")
    print("WPM: " + str(words_per_minute(words_arr)))
    print("Duplicate Word Percent: " + str(duplicate_word_percentage(words_arr)) + "%")
    data = {
        "words": words,
        "filler_word_percent": filler_word_percentage(words_arr, FILLER_WORDS),
        "average_wpm": words_per_minute(words_arr),
        "duplicate_word_percent": duplicate_word_percentage(words_arr),
        "speech_as_text": words,
        "bluemix_sentiments": response,

    }
    return data



def main():
    get_json_analysis_results()

if __name__ == '__main__':
    main()
