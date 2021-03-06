"""Tinkering Audio - Contract 4."""
import wave
import struct
import math
import pygame
import sys
from pygame.locals import *

pygame.init()
pygame.display.set_mode((200, 200))


class UIAudioGenerator:
    """Class for a whole script."""

    output_file_name = ["start_game.wav", "options.wav", "quit.wav"]
    sound_characteristic = ["positive", "neutral", "negative"]
    length_of_file_in_seconds = [0.5, 0.2, 0.8]

    CHANNEL_COUNT = 1
    SAMPLE_WIDTH = 2  # 2 bytes per sample
    SAMPLE_RATE = 44100
    COMPRESSION_TYPE = 'NONE'
    COMPRESSION_NAME = 'not compressed'
    MAX_VALUE = 32767
    FREQUENCY = 1500
    VOLUME = 0.5
    default_frequency = 1500

    def sound_preparation(self):
        """
        Script sets up files and passes them to another script.

        :return: No return.
        """
        for i in range(len(self.output_file_name)):
            sound_output = wave.open(self.output_file_name[i], 'w')

            sample_length = int(self.SAMPLE_RATE *
                                self.length_of_file_in_seconds[i]
                                )

            sound_characteristic = self.sound_characteristic[i]

            sound_output.setparams((self.CHANNEL_COUNT, self.SAMPLE_WIDTH,
                                    self.SAMPLE_RATE, sample_length,
                                    self.COMPRESSION_TYPE,
                                    self.COMPRESSION_NAME)
                                   )

            self.create_sound(UIAudioGenerator, sound_output,
                              sample_length, sound_characteristic
                              )

    def positive_sound(self, sample_length, loop_value):
        """
        Function makes sound sound friendly and positive.

        :param sample_length: Used to check at what stage sound modification is
        :param loop_value: Shows what point script is at
        :return: Modifies frequency value
        """
        if loop_value > sample_length * 0.25:
            if self.FREQUENCY < 3000:
                self.FREQUENCY += 0.1

    def neutral_sound(self, sample_length, loop_value):
        """
        Function makes neutral feedback sound.

        :param sample_length: Used to check at what stage sound modification is
        :param loop_value: Shows what point script is at
        :return: Modifies frequency value
        """
        if loop_value < sample_length * 0.3:
            self.FREQUENCY = 700
        elif loop_value < sample_length * 0.6:
            self.FREQUENCY = 1100
        elif loop_value < sample_length * 1:
            self.FREQUENCY = 700

    def negative_sound(self, sample_length, loop_value):
        """
        Function makes negative, decline like sound.

        :param sample_length: Used to check at what stage sound modification is
        :param loop_value: Shows what point script is at
        :return: Modifies frequency value
        """
        length_of_first_note = sample_length * 0.3
        length_of_second_note = sample_length * 0.5

        if loop_value < length_of_first_note:
            self.FREQUENCY = 2000
        elif loop_value < length_of_second_note:
            self.FREQUENCY = 600
        else:
            self.FREQUENCY = 200

    def create_sound(self, sound_output, sample_length, sound_characteristic):
        """
        Function that creates sound and exports sound file.

        :param sound_output: Reference to a sound file.
        :param sample_length: Length of certain sound file.
        :param sound_characteristic: Characteristic of certain sound file.
        :return: Function exports sound files.
        """
        self.FREQUENCY = self.default_frequency
        values = []

        for i in range(0, sample_length):
            if sound_characteristic == "positive":
                self.positive_sound(UIAudioGenerator, sample_length, i)
            elif sound_characteristic == "negative":
                self.negative_sound(UIAudioGenerator, sample_length, i)
            elif sound_characteristic == "neutral":
                self.neutral_sound(UIAudioGenerator, sample_length, i)

            value = math.sin(2.0 * math.pi * self.FREQUENCY *
                             (i / self.SAMPLE_RATE)) * (self.VOLUME *
                                                        self.MAX_VALUE)

            packed_value = struct.pack('h', int(value))

            for j in range(0, self.CHANNEL_COUNT):
                values.append(packed_value)

        sound_output.writeframes(b''.join(values))
        sound_output.close()


UIAudioGenerator.sound_preparation(UIAudioGenerator)

sound = pygame.mixer.Sound(UIAudioGenerator.output_file_name[0])
sound1 = pygame.mixer.Sound(UIAudioGenerator.output_file_name[1])
sound2 = pygame.mixer.Sound(UIAudioGenerator.output_file_name[2])


def main():
    """Main loop of the game."""
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYUP:
                if event.key == K_1:
                    sound.stop()
                    sound.play()
                if event.key == K_2:
                    sound1.stop()
                    sound1.play()
                if event.key == K_3:
                    sound2.stop()
                    sound2.play()


if __name__ == "__main__":
    main()
