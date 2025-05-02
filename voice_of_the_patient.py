#step1: Setup Audio recorder {ffmpeg & portaudio}
#ffmpeg,portaudio,pyaudio
import logging 
import speech_recognition as sr
from pydub import AudioSegment
from io import BytesIO

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s')

from speech_recognition import WaitTimeoutError

def record_audio(file_path, timeout=20, pharse_time_limit=None, retries=3):
    recognizer = sr.Recognizer()

    for attempt in range(retries):
        try:
            with sr.Microphone() as source:
                logging.info("Adjusting for ambient noise...")
                recognizer.adjust_for_ambient_noise(source, duration=1)
                logging.info(f"Attempt {attempt + 1}: Start speaking now...")

                audio_data = recognizer.listen(source, timeout=timeout, phrase_time_limit=pharse_time_limit)
                logging.info("Recording complete.")

                logging.info("Getting raw WAV data...")
                wav_data = audio_data.get_wav_data()

                logging.info("Converting WAV to AudioSegment...")
                audio_segment = AudioSegment.from_wav(BytesIO(wav_data))

                logging.info("Exporting to WAV...")
                audio_segment.export(file_path.replace(".mp3", ".wav"), format="wav")

                logging.info(f"Audio saved to {file_path.replace('.mp3', '.wav')}")
                print("Script execution finished.")
                break

        except sr.WaitTimeoutError:
            logging.warning("No speech detected. Trying again...")
        except Exception as e:
            logging.error("An unexpected error occurred", exc_info=True)
            break
    else:
        logging.error("Recording failed after multiple attempts.")

audio_file_path = "patient_voice_test.wav"  # <- use .wav not .mp3
record_audio(file_path=audio_file_path)     

# Step 2: Setup STT
import os 
from groq import Groq

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
def transcribe_with_groq(stt_model, audio_file_path,GROQ_API_KEY):
    client = Groq(api_key=GROQ_API_KEY)
    stt_model = "whisper-large-v3"

    with open(audio_file_path, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            model=stt_model,
            file=audio_file,
            language="en"
        )

    return transcription.text
