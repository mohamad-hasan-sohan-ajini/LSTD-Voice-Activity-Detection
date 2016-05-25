# -*- coding: utf-8 -*-
import numpy as np
import socket
import matplotlib.pyplot as plt
import threading
import time
from LSTD import *
from copy import deepcopy


# global varibles
WINDOW_DURATION = 3
Fs = 48000
BUFFER_SIZE = int(Fs * WINDOW_DURATION)
CHUNK = Fs / 100

plt.ion()
fig = plt.figure()
ax = fig.add_subplot(2, 1, 1)
short_ax = fig.add_subplot(2, 1, 2)

x = np.array(range(BUFFER_SIZE), dtype=float) / Fs
y = np.zeros(BUFFER_SIZE)
short_x = np.array(range(int(Fs * 0.1)), dtype=float) / Fs
short_x_len = short_x.shape[0]

line1, = ax.plot(x, y)
line2, = ax.plot(short_x, y[-short_x_len:])
l = threading.Lock()


def update_plot(vad=False):
    global x, y, ax, fig, line1
    l.acquire()
    tmp = y
    l.release()

    line1.set_ydata(tmp)
    line2.set_ydata(tmp[-short_x_len:])

    ax.clear()
    short_ax.clear()

    ax.set_ylim(-1500, 1500)
    short_ax.set_ylim(-1000, 1000)

    ax.plot(x, tmp)
    if(vad):
        short_ax.plot(short_x, tmp[-short_x_len:], 'r')
    else:
        short_ax.plot(short_x, tmp[-short_x_len:])

    fig.canvas.draw()


class Server(threading.Thread):

    def __init__(self, p=8008, h='127.0.0.1'):
        super(Server, self).__init__()
        self._s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._host = h
        self._port = p
        self._s.bind((self._host, self._port))
        self._kill = True

    def run(self):
        global x, y, l
        while(self._kill):
            #print('@ server')
            pkt, (ip, port) = self._s.recvfrom(self._port)
            rcvarr = np.fromstring(pkt, dtype=np.int16)
            CHUNK = rcvarr.shape[0]
            l.acquire()
            y[0:-CHUNK] = y[CHUNK:]
            y[-CHUNK:] = np.fromstring(pkt, dtype=np.int16)
            l.release()


if(__name__ == '__main__'):
    ser = Server()
    ser.start()
    my_vad = LSTD_vad(Fs=Fs)
    time.sleep(3)
    l.acquire()
    tmp = deepcopy(y)
    l.release()
    my_vad.noise_spec(tmp)
    print('in while')
    i = 0
    try:
        t0 = time.time()
        while(time.time() - t0 < 1000):
            if(i < 11):
                update_plot()
            else:
                update_plot(True)
            l.acquire()
            tmp = y[-int(0.025 * Fs):]
            l.release()
            my_vad.update_LSTE(tmp)
            i = my_vad.compute_LSTD()
            print(i)
            #print('plot updated')
    except Exception as e:
        print(e)
    finally:
        ser._kill = False
        #print(y[-int(Fs * 0.025):])
