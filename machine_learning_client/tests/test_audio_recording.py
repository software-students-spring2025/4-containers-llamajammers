import threading
import wave
from unittest import mock  
from machine_learning_client.audio_recording import audio_recording 
# MOCKING PyAudio 

class FakeStream:
    def __init__(self):
        self.closed = False
        self.frames = []

    def read(self, chunk):
        return b'\x00' * chunk  # fake audio data

    def stop_stream(self):
        self.closed = True

    def close(self):
        pass

class FakePyAudio:
    def open(self, *args, **kwargs):
        return FakeStream()

    def get_sample_size(self, fmt):
        return 2  # 16-bit

    def terminate(self):
        pass

# TESTS

@mock.patch("pyaudio.PyAudio", return_value=FakePyAudio())
def test_audio_recording_fixed_duration(mock_py_audio, tmp_path):
    """Test fixed-length recording with no stop event."""
    output_path = tmp_path / "test_output.wav"
    filename = audio_recording(filename=str(output_path), stop_event=None, record_seconds=1)
    
    assert filename == str(output_path)
    assert output_path.exists()

    # Check it's a valid WAV file
    with wave.open(str(output_path), "rb") as wf:
        assert wf.getnchannels() == 1
        assert wf.getframerate() == 44100

@mock.patch("pyaudio.PyAudio", return_value=FakePyAudio())
def test_audio_recording_with_stop_event(mock_py_audio, tmp_path):
    """Test interactive recording using a stop event."""
    output_path = tmp_path / "test_stop_event.wav"
    stop_event = threading.Event()

    def stop_after_delay():
        import time
        time.sleep(0.1)
        stop_event.set()

    thread = threading.Thread(target=stop_after_delay)
    thread.start()

    filename = audio_recording(filename=str(output_path), stop_event=stop_event)
    thread.join()

    assert filename == str(output_path)
    assert output_path.exists()
