import sounddevice as sd
import soundfile as sf

def record_audio(filename="recording.wav", duration=5, fs=44100):
    """Record audio from the default microphone for a given duration."""
    print("Recording audio...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    sf.write(filename, recording, fs)
    print(f"Audio recorded and saved to {filename}")
    return filename
