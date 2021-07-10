import speech_recognition as sr

def playWAV(FILE_NAME, pos=0, clip=10)
    # use the audio file as the audio source
    r = sr.Recognizer()
    with sr.AudioFile(AUDIO_FILE) as source:
        audio = r.record(source, duration=clip, offset=pos)
                
def printWAV(FILE_NAME, pos=0, clip=10)
    # use the audio file as the audio source
    r = sr.Recognizer()
    text = ""
    with sr.AudioFile(AUDIO_FILE) as source:
        audio = r.record(source, duration=clip, offset=pos)
        # recognize speech using Google Speech Recognition
        try:
            text += r.recognize_google(audio) + "\n"
        except sr.UnknownValueError:
            text += "Could not understand audio\n"
        except sr.RequestError as e:
            text += "Could not request results; {0}".format(e)+ "\n"
    return text