# main.py
import os
from dotenv import load_dotenv
from src import config, recorder, transcriber, responder, gui

def cli_mode():
    print("=== Running in CLI mode ===")
    try:
        # Record audio and save to a file (returns file path)
        audio_file = recorder.record_audio(duration=5)  # record for 5 seconds
        transcript = transcriber.transcribe(audio_file)
        answer = responder.generate_response(transcript)
        print("\nTranscript:")
        print(transcript)
        print("\nGenerated Answer:")
        print(answer)
    except Exception as e:
        print(f"Error during CLI processing: {e}")

def main():
    load_dotenv()  # Load OPENAI_API_KEY etc.
    mode = config.MODE  # 'cli' or 'gui'
    
    if mode == 'cli':
        cli_mode()
    else:
        gui.run_gui()

if __name__ == '__main__':
    main()
