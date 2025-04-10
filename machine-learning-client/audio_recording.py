"""Use PyAudio to record audio interactively with a stop event."""

import wave
import logging
import pyaudio
import time


def audio_recording(filename="recording.wav", stop_event=None, record_seconds=60):
    """Use PyAudio for recording audio and saving as a wave file."""
    # from PyAudio Installation guide
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100  # not sure what is optimal for audio recording (Maya) (I think it worked just fine when I tested it! -Polina)
    # RECORD_SECONDS = 60  # should we change to 1 minute? -> can also be parameter in the definition -Maya // so I would rather use it interactively with a stop event! -Polina

    # pylint: disable=no-member
    # ^ suppressing an error with pylint but I don't think this is an issue at runtime

    pa = pyaudio.PyAudio()
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(pa.get_sample_size(FORMAT))
        wf.setframerate(RATE)

        # Attempt to open the audio input stream; if unavailable, log an error and use pre-recorded file.
        try:
            stream = pa.open(
                format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK,
            )
        except OSError as e:
            logging.error("No audio input device found, using pre-recorded file instead. Error: %s", e)
            pa.terminate()
            return "recording.wav"

        logging.info("Recording started...")

        try:
            if stop_event is None:
                # Use fixed duration recording if no event is provided
                for _ in range(0, int(RATE / CHUNK * record_seconds)):
                    wf.writeframes(stream.read(CHUNK))
            else:
                while not stop_event.is_set():
                    try:
                        data = stream.read(CHUNK)
                        wf.writeframes(data)
                    except Exception as e:
                        logging.error("Error reading from stream: %s", e)
                        break
        finally:
            logging.info("Recording stopped.")
            stream.stop_stream()
            stream.close()
            pa.terminate()
    return filename

if __name__ == "__main__":
    audio_recording("test_recording.wav")
    print("Audio saved to test_recording.wav")
