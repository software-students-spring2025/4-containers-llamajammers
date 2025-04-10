"""Use PyAudio to record audio interactively with a stop event."""

import wave
import pyaudio
import time


def audio_recording(filename="recording.wav", stop_event=None):
    """Use PyAudio for recording audio and saving as a wave file"""
    # from PyAudio Installation guide
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100  # not sure what is optimal for audio recording (Maya) (I think it worked just fine when I tested  it! -Polina)
    RECORD_SECONDS = 60  # should we change to 1 minute? -> can also be parameter in the definition -Maya // so I would rather use it interactively with a stop event! -Polina
    

    # pylint: disable=no-member
    # ^ suppressing an error with pylint but i dont think this is an issue at runtime

    pa = pyaudio.PyAudio()
    wf = wave.open(filename, "wb")
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(pa.get_sample_size(FORMAT))
    wf.setframerate(RATE)

    stream = pa.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    print("Recording started...")
    
    if stop_event is None:
        # fixed time-wise recording provided if no stop event
        for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            wf.writeframes(stream.read(CHUNK))
    else:
        # so we are going to keep recording until stop_event is set
        while not stop_event.is_set():
            try:
                data = stream.read(CHUNK)
                wf.writeframes(data)
            except Exception as e:
                print("Error reading from stream:", e)
                break

    print("Recording stopped.")
    stream.stop_stream()
    stream.close()
    pa.terminate()
    wf.close()
    return filename

if __name__ == "__main__":
    audio_recording("test_recording.wav")
    print("Audio saved to test_recording.wav")
