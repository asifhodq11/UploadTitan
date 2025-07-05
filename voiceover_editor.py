import pyttsx3
from pydub import AudioSegment
from script_generator import generate_script
from job_logger import log_event

MAX_DURATION = 40  # seconds

def generate_voiceover(script=None, output_file="voiceover.mp3"):
    if script is None:
        script = generate_script()

    engine = pyttsx3.init()
    engine.setProperty('rate', 175)
    engine.save_to_file(script, "temp_voice.wav")
    engine.runAndWait()

    # Convert to MP3 and trim if needed
    audio = AudioSegment.from_wav("temp_voice.wav")
    duration = len(audio) / 1000  # in seconds

    if duration > MAX_DURATION:
        audio = audio[:MAX_DURATION * 1000]

    audio.export(output_file, format="mp3")
    log_event("Voiceover Generated", f"{output_file} (duration: {min(duration, MAX_DURATION)}s)")

    return output_file
