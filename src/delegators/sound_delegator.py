from __future__ import annotations
import math
import array
import numpy as np
import pydub
from re import L
from pydub import AudioSegment
from src.helpers.sound.sound_helper import SoundHelper


class SoundDelegator:
    def __init__(self) -> None:
        self.sound = None
    
    def load(self, path: str, file_type: str) -> SoundDelegator:
        self.sound = SoundHelper.load(path=path, file_type=file_type)
        return self
    
    def apply_filters(self, filters: dict) -> SoundDelegator:
        for key, value in filters.items():
            getattr(self, f'_{key}')(value)
        return self
    
    def _high_fq(self, frequency: float) -> SoundDelegator:
        """applying max frequency for a specific instrument"""
        # original = self.sound.get_array_of_samples()
        # filteredArray = array.array(self.sound.array_type, original)
        # fourier = np.fft.fft(original)
        # for index, freq in enumerate(fourier):
        #     if math.fabs(freq.real) > frequency:
        #         fourier[index] = freq.real / math.fabs(freq.real) * frequency + 1j * freq.imag
        # filtered_array = np.fft.ifft(fourier)
        # filtered_array = [int(a.real) for a in filtered_array]
        # filtered_array = array.array(self.sound.array_type, filtered_array)
        # self.sound = self.sound._spawn(data=filtered_array)
        self.sound = pydub.effects.low_pass_filter(self.sound, frequency)
        return self
    
    def _low_fq(self, frequency: float) -> SoundDelegator:
        """applying min frequency for a specific instrument"""
        self.sound = pydub.effects.high_pass_filter(self.sound, frequency)
        return self

    def mix(self, sound: AudioSegment) -> SoundDelegator:
        if sound is not None:
            self.sound = SoundHelper.mix(sound, self.sound)
        return self

    def get(self) -> AudioSegment:
        return self.sound


def low_pass_filter(seg, cutoff):
    """
        cutoff - Frequency (in Hz) where higher frequency signal will begin to
            be reduced by 6dB per octave (doubling in frequency) above this point
    """
    RC = 1.0 / (cutoff * 2 * math.pi)
    dt = 1.0 / seg.frame_rate

    alpha = dt / (RC + dt)
    
    original = seg.get_array_of_samples()
    filteredArray = array.array(seg.array_type, original)
    
    frame_count = int(seg.frame_count())

    last_val = [0] * seg.channels
    for i in range(seg.channels):
        last_val[i] = filteredArray[i] = original[i]

    for i in range(1, frame_count):
        for j in range(seg.channels):
            offset = (i * seg.channels) + j
            last_val[j] = last_val[j] + (alpha * (original[offset] - last_val[j]))
            filteredArray[offset] = int(last_val[j])

    return seg._spawn(data=filteredArray)