"""

import httplib as http
from urllib import urlencode
import json
import base64
# from tokens import *

# Debug audio: Just to play wav from this module
import pyaudio
import wave
import pyglet

# Note: Use the subscription key as Client secret below.
clientSecret = '2f3bcd576a404153a32724a54e7d6e6b'

ttsHost = "https://speech.platform.bing.com"

params = urlencode(
    {'grant_type': 'client_credentials', 'client_id': 'nothing', 'client_secret': clientSecret, 'scope': ttsHost})

# print ("The body data: %s" % (params))

headers = {"Content-type": "application/x-www-form-urlencoded"}

AccessTokenHost = "oxford-speech.cloudapp.net"
path = "/token/issueToken"

# Connect to server to get the Oxford Access Token
conn = http.HTTPSConnection(AccessTokenHost)
conn.request("POST", path, params, headers)
response = conn.getresponse()

# print response.status, response.reason

data = response.read()
conn.close()

accesstoken = data.decode("UTF-8")
print ("Oxford Access Token: " + accesstoken)

# decode the object from json
ddata = json.loads(accesstoken)
access_token = ddata['access_token']

headers = {"Content-type"            : "application/ssml+xml",
           "X-Microsoft-OutputFormat": "riff-16khz-16bit-mono-pcm",
           "Authorization"           : "Bearer " + access_token,
           "X-Search-AppId"          : "07D3234E49CE426DAA29772419F436CA",
           "X-Search-ClientID"       : "1ECFAE91408841A480F00935DC390960",
           "User-Agent"              : "TTSForPython"}


def get_raw_wav(text):
    print "DEBUG TEXT:", text
    body = "<speak version='1.0' xml:lang='en-us'><voice xml:lang='en-us'" \
           "xml:gender='Female' name='Microsoft Server Speech Text to Speech Voice (en-US, ZiraRUS)'>" + text + "</voice></speak>"

    conn = http.HTTPSConnection("speech.platform.bing.com")
    conn.request("POST", "/synthesize", body, headers)

    response = conn.getresponse()
    print(response.status, response.reason)

    data_ = response.read()
    conn.close()

    encoded = base64.b64encode(data_)
    s = str(encoded)
    sliced = s[2:-1]

    f = open('file.wav', 'w')
    f.write(data_)

    # print(sliced)
    return data_


if __name__ == "__main__":
    get_raw_wav('Hello my name is bryan.')

    # song = pyglet.media.load('file.wav')
    # song.play()
    # pyglet.app.run()

"""


