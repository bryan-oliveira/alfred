import speech_recognition as sr
from config import UPLOAD_FOLDER
import os

BING_KEY = "2f3bcd576a404153a32724a54e7d6e6b"


def speech_recognition_from_microphone():

    r = sr.Recognizer()

    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    try:
        return r.recognize_bing(audio, key=BING_KEY)
    except sr.UnknownValueError:
        return "Alfred: I could not understand."
    except sr.RequestError as e:
        return "Could not request results from Microsoft Bing Voice Recognition service; {0}".format(e)


def speech_recognition_from_file():

    folder_path = UPLOAD_FOLDER

    file_to_convert = folder_path + "test.ogg"
    new_file = os.path.join(folder_path, 'test.wav')

    # Verbose level of ffmpeg
    verbosity = " -nostats -loglevel 3"

    os.system("ffmpeg" + verbosity + " -y -i " + file_to_convert + " -ar 8000 " + new_file)

    # Debug info
    # print "#####", os.system("ffmpeg" + verbosity + " -y -i " + file_to_convert + " -ar 8000 " + new_file)
    # print "FILE ### ", new_file
    # os.system("chmod 666 audio/*")
    # print os.system("ls -la audio")

    r = sr.Recognizer()

    with sr.AudioFile(new_file) as wav:
        audio = r.record(wav)
        try:
            return r.recognize_bing(audio, key=BING_KEY)
        except sr.UnknownValueError:
            return "Alfred: I could not understand."
        except sr.RequestError as e:
            return "Could not request results from Microsoft Bing Voice Recognition service; {0}".format(e)

