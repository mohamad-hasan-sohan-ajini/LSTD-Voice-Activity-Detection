# -*- coding: utf-8 -*-
import numpy as np
import scipy
from scipy.fft import fft


class LSTD_vad(object):

    def __init__(self, win_len=0.025, win_step=0.01, Fs=16000, N=5, NFFT=512):
        self._win_len = win_len
        self._win_step = win_step
        self._Fs = Fs
        self._N = 5
        self._NFFT = NFFT
        # sample per window = window lngth * sampling freq.
        self._spw = int(win_len * Fs)
        # sample per window step = window step * sampling freq.
        self._sps = int(win_step * Fs)
        self._window = np.hamming(self._spw)
        # memory of prev specs
        self._last_specs = []
        self._lste = None

    def noise_spec(self, noise_signal):
        '''
        calculate noise spectrum
        input:
            noise_signal -> noisy signal, at least N (LSTE order) frame
        '''
        if(noise_signal.shape[0] < self._spw + self._sps * self._N):
            raise Exception('low information about noise')
        signal_len = noise_signal.shape[0]
        noise_spec = fft(noise_signal[:self._spw], self._NFFT)
        for i in range(1, int((signal_len - self._spw) / self._sps)):
            start = self._sps * i
            end = start + self._spw
            self._last_specs.append(np.abs(fft(noise_signal[start:end], self._NFFT)) ** 2)
            noise_spec += self._last_specs[-1]
        noise_spec /= int((signal_len - self._spw) / self._sps)
        self._last_specs = self._last_specs[-self._N:]
        self._noise_spec = np.array(np.abs(noise_spec), float)

    def update_LSTE(self, frame):
        '''
        calculate lste for current frame
        input:
            frame -> np array of length win_len * Fs
        '''
        if(frame.shape[0] != self._spw):
            print('exception')
            raise Exception('samples not expected')
        self._last_specs.append(np.abs(fft(frame, self._NFFT)) ** 2)
        self._last_specs = self._last_specs[-self._N:]
        self._lste = np.array(np.array(self._last_specs).max(axis=0), float)

    def compute_LSTD(self):
        result = 10.0 * np.log10(np.sum(self._lste / self._noise_spec) / self._NFFT)
        return result
