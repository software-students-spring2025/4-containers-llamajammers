"""Use PyAudio to record audio"""

import pyaudio
import wave
import sys

# from PyAudio Installation guide
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1 if sys.platform == "darwin" else 2
RATE = 44100
RECORD_SECONDS = 5  # should we change to 1 minute?

audio = pyaudio.PyAudio()
