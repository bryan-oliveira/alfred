#!/usr/bin/python


"""

import alsaaudio
import time
import audioop

# Monitor environment noise level. This will set the baseline
env_noise_level = []

# Open the device in nonblocking capture mode. On my system the microfone I am using is card2.
# This can be checked in console: arecord -l
inp = alsaaudio.PCM(type=alsaaudio.PCM_CAPTURE, mode=alsaaudio.PCM_NONBLOCK, device='default', cardindex=2)


# Set attributes: Mono, 8000 Hz, 16 bit little endian samples
inp.setchannels(1)
inp.setrate(8000)
inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
inp.setperiodsize(1600)

while True:
    # Read data from device
    l, data = inp.read()
    if l:
        # Return the maximum of the absolute value of all samples in a fragment.
        print l, audioop.max(data, 2)
    time.sleep(.1)

"""