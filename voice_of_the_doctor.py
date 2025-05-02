#step1a :setup text to speech-TTS-model(gTTS)
import os
from gtts import gTTS



def text_to_speech_with_gtts_old(input_text,output_filepath):
    language="en"

    audioobj = gTTS(
        text=input_text,
        lang=language,
        slow=False
    )
    audioobj.save(output_filepath)

input_text="Hi this is AI with Halima"
# text_to_speech_with_gtts(input_text=input_text,output_filepath="gtts_testing.mp3")
#step1b :setup text to speech-TTS-model(Elevation)
# Step1b: Setup Text to Speech - ElevenLabs
import elevenlabs
from elevenlabs.client import ElevenLabs
import os

ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")

def text_to_speech_with_elevenlabs_old(input_text, output_filepath):
    client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
    audio = client.generate(
        text=input_text,
        voice="Aria",
        output_format="mp3_22050_32",
        model="eleven_turbo_v2"
    )
    elevenlabs.save(audio, output_filepath)


# text_to_speech_with_elevenlabs(input_text, output_filepath="elevenlabs_testing.mp3")


    
#Step2: useMode; for Text output to voice
from gtts import gTTS
from pydub import AudioSegment
import platform
import subprocess
import os

def text_to_speech_with_gtts(input_text, output_filepath):
    language = "en"
    mp3_path = output_filepath
    wav_path = output_filepath.replace(".mp3", ".wav")

    # Generate and save MP3
    audioobj = gTTS(text=input_text, lang=language, slow=False)
    audioobj.save(mp3_path)

    # Convert MP3 to WAV
    sound = AudioSegment.from_mp3(mp3_path)
    sound.export(wav_path, format="wav")

    # Play WAV
    os_name = platform.system()
    try:
        if os_name == "Darwin":  # macOS
            subprocess.run(['afplay', wav_path])
        elif os_name == "Windows":  # Windows
            subprocess.run(['powershell', '-c', f'(New-Object Media.SoundPlayer "{wav_path}").PlaySync();'])
        elif os_name == "Linux":
            subprocess.run(['aplay', wav_path])
        else:
            raise OSError("Unsupported operating system")
    except Exception as e:
        print(f"An error occurred while trying to play the audio: {e}")





input_text="Hi this is AI with Halima,autoplay testing"
# text_to_speech_with_gtts(input_text=input_text,output_filepath="gtts_testing_autoplay.mp3")

def text_to_speech_with_elevenlabs(input_text, output_filepath_mp3):
    # Generate audio from ElevenLabs TTS
    client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
    audio = client.generate(
        text=input_text,
        voice="Aria",
        output_format="mp3_22050_32",
        model="eleven_turbo_v2"
    )
    elevenlabs.save(audio, output_filepath_mp3)

    # Convert MP3 to WAV for compatibility with Windows Media.SoundPlayer
    output_filepath_wav = output_filepath_mp3.replace(".mp3", ".wav")
    audio_segment = AudioSegment.from_mp3(output_filepath_mp3)
    audio_segment.export(output_filepath_wav, format="wav")

    # Play the WAV file based on OS
    os_name = platform.system()
    try:
        if os_name == "Darwin":  # macOS
            subprocess.run(['afplay', output_filepath_wav])
        elif os_name == "Windows":  # Windows
            subprocess.run(['powershell', '-c', f'(New-Object Media.SoundPlayer "{output_filepath_wav}").PlaySync();'])
        elif os_name == "Linux":
            subprocess.run(['aplay', output_filepath_wav])
        else:
            raise OSError("Unsupported operating system")
    except Exception as e:
        print(f"An error occurred while trying to play the audio: {e}")

# Example usage
#text_to_speech_with_elevenlabs("Hi, this is AI with Halima, ElevenLabs testing", "elevenlabs_testing.mp3")
text_to_speech_with_elevenlabs(input_text, output_filepath_mp3="elevenlabs_testing.mp3")
