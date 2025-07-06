import os
from pydub import AudioSegment
import pyttsx3

def generate_voiceover(text: str, output_path: str, max_duration: int = 40):
    """
    Generate a voiceover from text using pyttsx3 and trim to max_duration (in seconds).
    Output is saved as MP3.
    """
    try:
        temp_wav = "temp_voice.wav"

        # Initialize engine
        engine = pyttsx3.init()
        engine.save_to_file(text, temp_wav)
        engine.runAndWait()

        # Load WAV and trim to max_duration seconds
        audio = AudioSegment.from_wav(temp_wav)
        trimmed = audio[:max_duration * 1000]  # milliseconds
        trimmed.export(output_path, format="mp3")

        os.remove(temp_wav)
        print(f"[✅] Voiceover saved to {output_path}")
        return True

    except Exception as e:
        print(f"[❌] Voiceover generation failed: {e}")
        return False


# Example test
if __name__ == "__main__":
    sample_text = "Welcome to UploadTitan! This is a test voiceover."
    generate_voiceover(sample_text, "voiceover_test.mp3")
    
