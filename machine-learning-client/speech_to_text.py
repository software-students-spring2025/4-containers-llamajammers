"""Using Whisper from Open AI, converts an audio recording to text transcript."""

import whisper  # also need to install ffmpeg


def speech_to_text(recording):
    """Whisper is used for Audio Recording to text"""

    model = whisper.load_model(
        "medium"
    )  # chose turbo from whisper's README, may have other options
    transcript = model.transcribe(recording)

    return transcript["text"]


if __name__ == "__main__":
    # need to get audio from somewhere
    audio = audio_recording()  # need to implement something like this
    transcription = speech_to_text(audio)
    print(f"Transcription: {transcription}")
