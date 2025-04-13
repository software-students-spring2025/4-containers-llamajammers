"""Using Whisper from Open AI, converts an audio recording to text transcript."""

import logging
import whisper  # also need to install ffmpeg
from audio_recording import audio_recording

logging.basicConfig(level=logging.INFO)


def speech_to_text(recording):
    """Whisper is used for Audio Recording to text
    Args:
        recording (str): Path to the audio file.

    Returns:
        str: Transcribed text.
    """

    try:
        model = whisper.load_model("medium")
    except Exception as e:
        logging.error("Error loading Whisper model: %s", e)
        raise

    try:
        transcript = model.transcribe(recording)
    except Exception as e:
        logging.error("Error during transcription: %s", e)
        raise

    return transcript.get("text", "")


if __name__ == "__main__":
    # need to get audio from somewhere
    AUDIO = audio_recording(
        "test_recording.wav"
    )  # need to implement something like this
    transcription = speech_to_text(AUDIO)
    print(f"Transcription: {transcription}")
