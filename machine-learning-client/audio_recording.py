"""Use PyAudio to record audio"""

import wave
import pyaudio


def audio_recording(filename="recording.wav"):
    """Use PyAudio for recording audio and saving as a wave file"""
    # from PyAudio Installation guide
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100  # not sure what is optimal for audio recording
    RECORD_SECONDS = 5  # should we change to 1 minute?

    # pylint: disable=no-member
    # ^ suppressing an error with pylint but i dont think this is an issue at runtime
    with wave.open(filename, "wb") as wf:
        audio = pyaudio.PyAudio()
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)

        stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True)

        print("Recording...")
        for _ in range(0, RATE // CHUNK * RECORD_SECONDS):
            wf.writeframes(stream.read(CHUNK))

    stream.close()
    audio.terminate()

    return filename


if __name__ == "__main__":
    recording = audio_recording()  # Records for 5 seconds
    print(f"Audio saved to {recording}")
