# MHacks X
# Speak - Speech Recognition

import contextlib
import wave
from os import path
import speech_recognition as sr

AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "english.wav")
FILLER_WORDS = ["ah", "um", "uh", "so", "and", "oh", "like", "you know", "I mean"]
# AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "computer_two_hours.wav")
# AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "egotistical.wav")
# AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "hawking01.wav")

# use the audio file as the audio source

r = sr.Recognizer()


def acquire_audio():
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


def words_per_minute(file_name, word_arr):
    duration = audio_duration(file_name)
    word_count = len(word_arr)
    return (float(word_count) / duration) * 60


def duplicate_word_percentage(words_arr):
    words_as_set = set(words_arr)
    duplicates = len(words_arr) - len(words_as_set)
    duplicate_percent = (float(duplicates) / len(words_arr)) * 100
    return duplicate_percent


def main():
    audio = acquire_audio()
    words = sphinx_extract_text(audio)
    print("Input: " + AUDIO_FILE)
    print("Output: " + words)
    # print("Google: " + google_speech_extract_text(audio))
    words_arr = words.split(" ")
    words_arr[0] = "uh"
    words_arr[1] = "uh"
    # print(len(words_arr))
    print("Filler word percent: " + str(filler_word_percentage(words_arr, FILLER_WORDS)) + "%")
    print("WPM: " + str(words_per_minute(AUDIO_FILE, words_arr)))
    print("Duplicate Word Percent: " + str(duplicate_word_percentage(words_arr)) + "%")


if __name__ == '__main__':
    main()
