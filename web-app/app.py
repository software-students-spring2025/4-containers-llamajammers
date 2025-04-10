import os
import sys
import threading
#import wave
import re
#import time
from datetime import datetime

from flask import Flask, render_template_string, jsonify
from pymongo import MongoClient
#import pyaudio
#import whisper
# Add the machine-learning-client directory to the Python path
current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)
ml_client_path = os.path.join(parent_dir, "machine-learning-client")
sys.path.append(ml_client_path)

from audio_recording import audio_recording
from speech_to_text import speech_to_text

app = Flask(__name__)
#recording_thread = None
#stop_recording_event = None
RECORDING_FILENAME = "recording.wav" # or should it be "../machine-learning-client/recording.wav"

# MongoDB connection 
client = MongoClient("mongodb://localhost:27017/")
db = client['filler_words_detection']
recordings_collection = db['recordings']

# Load the Whisper model (NOT ANYMORE => implemented in ml client folder instead)
#whisper_model = whisper.load_model("medium") # chose medium for now

# List of filler words to detect (can add more later)
FILLER_WORDS = [
    "um", "uh", "like", "you know", "so", "well", "I mean",
    "just", "basically", "sort of", "kind of", "hmm", "I guess", "yeah", "right", "basically"
]


# HTML Template for the Main Page
MAIN_PAGE_TEMPLATE = """
<!doctype html>
<html lang="en">
  <head>
    <title>Filler Words Detection</title>
    <style>
      body { font-family: Arial, sans-serif; margin: 30px; }
      h1 { color: #333; }
      button { padding: 10px 20px; font-size: 16px; margin: 5px; }
      #summary { margin-top: 20px; font-size: 18px; }
    </style>
    <script>
      function startRecording() {
        document.getElementById("status").innerText = "Recording started...";
        fetch("/start_recording")
          .then(response => response.json())
          .then(data => {});
      }

      function stopRecording() {
        document.getElementById("status").innerText = "Processing...";
        fetch("/stop_recording")
          .then(response => response.json())
          .then(data => {
            document.getElementById("summary").innerText = data.summary;
            document.getElementById("status").innerText = "";
            if (data.success) {
              document.getElementById("transcript_btn").style.display = "inline-block";
            }
          });
      }
    </script>
  </head>
  <body>
    <h1>Filler Words Detection</h1>
    <button onclick="startRecording()">Start Recording</button>
    <button onclick="stopRecording()">Stop Recording</button>
    <div id="status"></div>
    <div id="summary"></div>
    <br>
    <button id="transcript_btn" onclick="window.location.href='/transcript'" style="display:none;">See the Transcript</button>
  </body>
</html>
"""

# FUNCTIONS
def count_filler_words(transcript):
    """Count total occurrences of filler words in the transcript."""
    total = 0
    transcript_lower = transcript.lower()
    for word in FILLER_WORDS:
        pattern = r'\b' + re.escape(word) + r'\b'
        matches = re.findall(pattern, transcript_lower)
        total += len(matches)
    return total

# global variables
recording_thread = None
stop_recording_event = None

@app.route("/")
def index():
    return render_template_string(MAIN_PAGE_TEMPLATE)

@app.route("/start_recording", methods=["GET"])
def start_recording():
    global recording_thread, stop_recording_event
    stop_recording_event = threading.Event()
    # Start the interactive recording in a background thread
    recording_thread = threading.Thread(target=audio_recording, args=(RECORDING_FILENAME, stop_recording_event))
    recording_thread.start()
    return jsonify({"status": "recording started"})

@app.route("/stop_recording", methods=["GET"])
def stop_recording():
    global recording_thread, stop_recording_event

    if stop_recording_event:
        stop_recording_event.set() 
    if recording_thread:
        recording_thread.join()

    try:
        transcript = speech_to_text(RECORDING_FILENAME)
    except Exception as e:
        transcript = f"Error during transcription: {e}"

    filler_count = count_filler_words(transcript)
    record_data = {
        "timestamp": datetime.utcnow(),
        "transcript": transcript,
        "filler_count": filler_count,
        "detailed_counts": {
            word: len(re.findall(r'\b' + re.escape(word) + r'\b', transcript.lower()))
            for word in FILLER_WORDS
        }
    }
    recordings_collection.insert_one(record_data)
    summary = f"Detected {filler_count} filler words in your recording."
    return jsonify({"success": True, "summary": summary})

@app.route("/transcript", methods=["GET"])
def transcript():
    doc = recordings_collection.find_one(sort=[("timestamp", -1)])
    if doc is None:
        transcript_text = "No transcript available."
    else:
        transcript_text = doc.get("transcript", "Transcript not found.")

    def highlight_filler(text):
        for word in FILLER_WORDS:
            text = re.sub(r'(\b' + re.escape(word) + r'\b)', r'<b>\1</b>', text, flags=re.IGNORECASE)
        return text

    transcript_highlighted = highlight_filler(transcript_text)
    transcript_page = f"""
    <!doctype html>
    <html lang="en">
      <head>
        <title>Transcript</title>
        <style>
          body {{ font-family: Arial, sans-serif; margin: 30px; }}
          h1 {{ color: #333; }}
          pre {{ background-color: #f8f8f8; padding: 15px; }}
        </style>
      </head>
      <body>
        <h1>Transcript</h1>
        <pre>{transcript_highlighted}</pre>
        <button onclick="window.location.href='/'">Back</button>
      </body>
    </html>
    """
    return transcript_page

if __name__ == "__main__":
    if os.path.exists(RECORDING_FILENAME):
        os.remove(RECORDING_FILENAME)
    app.run(debug=True, port=5000)