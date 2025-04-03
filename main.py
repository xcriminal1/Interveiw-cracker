import os
import sounddevice as sd
import numpy as np
import queue
import threading
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("Please set your GEMINI_API_KEY in the .env file or as an environment variable.")

genai.configure(api_key=GEMINI_API_KEY)

audio_queue = queue.Queue()
recording = True

# Audio settings
SAMPLE_RATE = 44100
CHANNELS = 1
BLOCK_SIZE = 1024

def callback(indata, frames, time, status):
    if status:
        print(status, flush=True)
    audio_queue.put(indata.copy())

def record_audio():
    """Continuously records audio and sends it for processing."""
    global recording
    with sd.InputStream(samplerate=SAMPLE_RATE, channels=CHANNELS, blocksize=BLOCK_SIZE, callback=callback):
        while recording:
            try:
                sd.sleep(50)  # Reduce CPU usage
            except KeyboardInterrupt:
                break

def process_audio():
    """Processes recorded audio and sends to Gemini for analysis."""
    while recording:
        try:
            audio_chunk = audio_queue.get(timeout=1)
            text = transcribe_audio(audio_chunk)
            if text:
                print("User: ", text)
                response = get_ai_response(text)
                print("AI: ", response)
        except queue.Empty:
            continue

def transcribe_audio(audio_data):
    """Simulates audio transcription."""
    return "Simulated transcription of spoken words."

def get_ai_response(text):
    """Gets AI-generated response based on transcribed text using Gemini API."""
    try:
        response = genai.generate_text(model="gemini-1.5-flash", prompt=text)
        return response.result.strip()
    except Exception as e:
        return f"Error generating response: {e}"

def main():
    """Starts real-time audio analysis."""
    global recording
    print("Starting real-time audio processing...")
    
    thread1 = threading.Thread(target=record_audio, daemon=True)
    thread2 = threading.Thread(target=process_audio, daemon=True)
    
    thread1.start()
    thread2.start()
    
    try:
        while True:
            sd.sleep(100)
    except KeyboardInterrupt:
        print("Stopping...")
        recording = False
        thread1.join()
        thread2.join()

if __name__ == "__main__":
    main()
