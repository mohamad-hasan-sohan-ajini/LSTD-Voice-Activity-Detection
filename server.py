# -*- coding: utf-8 -*-
import numpy as np
import socket
import scipy.io.wavfile as wav
import matplotlib.pyplot as plt


# make socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host = '127.0.0.1'
port = 8008
s.bind((host, port))

samples = []
try:
    while(len(samples) < 1000000):
        pkt, (ip, port) = s.recvfrom(port)
        print(len(pkt))
        samples.extend(np.fromstring(pkt, dtype=np.int16).tolist())
except:
    pass
finally:
    print('samples length {}'.format(len(samples)))
    samples = np.array(samples, dtype=np.int16)
    wav.write('test.wav', 48000, samples)
    plt.plot(samples)
    plt.show()
