import wave
import struct
import math

OUTPUT_FILENAME = "noise.wav"
LENGTH_OF_FILE_IN_SECONDS = 1
CHANNEL_COUNT = 1
SAMPLE_WIDTH = 2  # 2 bytes per sample
SAMPLE_RATE = 44100
SAMPLE_LENGTH = SAMPLE_RATE * LENGTH_OF_FILE_IN_SECONDS
COMPRESSION_TYPE = 'NONE'
COMPRESSION_NAME = 'not compressed'
MAX_VALUE = 32767
FREQUENCY = 15000

noise_out = wave.open(OUTPUT_FILENAME, 'w')
noise_out.setparams((CHANNEL_COUNT, SAMPLE_WIDTH, SAMPLE_RATE,
SAMPLE_LENGTH, 'NONE', 'not compressed'))

values = []

for i in range(0, SAMPLE_LENGTH):
    value = math.sin(2.0 * math.pi * FREQUENCY * (i / SAMPLE_RATE)) * MAX_VALUE
    packed_value = struct.pack('h', int(value))
    for j in range(0, CHANNEL_COUNT):
        values.append(packed_value)

noise_out.writeframes(b''.join(values))
noise_out.close()
