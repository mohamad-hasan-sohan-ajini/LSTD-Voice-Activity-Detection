# -*- coding: utf-8 -*-
"""
PyAudio Example: Make a wire between input and output (i.e., record a
few samples and play them back immediately).

This is the callback (non-blocking) version.
"""

import pyaudio
import time
import socket

WIDTH = 2
CHANNELS = 1
RATE = 48000
CHUNK = RATE / 100

p = pyaudio.PyAudio()
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host = '127.0.0.1'
port = 8008


def callback(in_data, frame_count, time_info, status):
    #print('in_data\n{}\n---------\n\n'.format(np.fromstring(in_data, dtype=np.int16)))
    s.sendto(in_data, (host, port))
    return (in_data, pyaudio.paContinue)

stream = p.open(format=p.get_format_from_width(WIDTH),
                channels=CHANNELS,
                rate=RATE,
                input=True,
                output=True,
                frames_per_buffer=CHUNK,
                stream_callback=callback)

stream.start_stream()


while stream.is_active():
    time.sleep(0.3)

stream.stop_stream()
stream.close()
p.terminate()
