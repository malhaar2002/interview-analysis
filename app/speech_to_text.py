import speech_recognition as sr
from pydub import AudioSegment
import assemblyai as aai
from secret import assemblyai_key

def transcribe_video_file(VIDEO_FILE):
    # Load the video file
    video = AudioSegment.from_file(VIDEO_FILE, format="mp4")
    audio = video.set_channels(1).set_frame_rate(16000).set_sample_width(2)
    audio.export("audio.wav", format="wav")

    # Replace with your API token
    aai.settings.api_key = assemblyai_key

    # URL of the file to transcribe
    FILE_URL = "audio.wav"

    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(FILE_URL)

    return transcript.text
