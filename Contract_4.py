"""Tinkering audio contract4 by:
Konrad Kowalewski - main Driver
Joachim Rayski - Navigator and occasional Driver
"""
import wave
import struct
import math
import pygame
import sys
import random
from pygame.locals import *

pygame.init()
pygame.display.set_mode((200, 200))


class UIAudioGenerator:
    OUTPUT_FILENAME = "noise.wav"
    LENGTH_OF_FILE_IN_SECONDS = 0.2
    CHANNEL_COUNT = 1
    SAMPLE_WIDTH = 2  # 2 bytes per sample
    SAMPLE_RATE = 44100
    SAMPLE_LENGTH = int(SAMPLE_RATE * LENGTH_OF_FILE_IN_SECONDS)
    COMPRESSION_TYPE = 'NONE'
    COMPRESSION_NAME = 'not compressed'
    MAX_VALUE = 32767
    FREQUENCY = 1500
    VOLUME = 0.5

    noise_out = wave.open(OUTPUT_FILENAME, 'w')
    noise_out.setparams((CHANNEL_COUNT, SAMPLE_WIDTH, SAMPLE_RATE,
    SAMPLE_LENGTH, 'NONE', 'not compressed'))


    values = []

    def create_sound(self):
        for i in range(0, self.SAMPLE_LENGTH):
            if i > self.SAMPLE_LENGTH * 0.25:
                if self.FREQUENCY < 3000:
                    self.FREQUENCY += 0.1
            if i < self.SAMPLE_LENGTH * 0.2:
                self.FREQUENCY = random.randint(1000, 3000)
            value = math.sin(2.0 * math.pi * self.FREQUENCY * (i / self.SAMPLE_RATE)) * (self.VOLUME * self.MAX_VALUE)
            packed_value = struct.pack('h', int(value))
            for j in range(0, self.CHANNEL_COUNT):
                self.values.append(packed_value)

        self.noise_out.writeframes(b''.join(self.values))
        self.noise_out.close()


UIAudioGenerator.create_sound(UIAudioGenerator)
sound = pygame.mixer.Sound(UIAudioGenerator.OUTPUT_FILENAME)


def main():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYUP:
                if event.key == K_1:
                    sound.stop()
                    sound.play()


if __name__ == "__main__":
    main()