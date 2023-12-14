import speech_recognition as sr
from pydub import AudioSegment
import assemblyai as aai

# Load the video file
video = AudioSegment.from_file("rushil.mp4", format="mp4")
audio = video.set_channels(1).set_frame_rate(16000).set_sample_width(2)
audio.export("audio.wav", format="wav")

# Replace with your API token
aai.settings.api_key = f"fb54b4215a7c4f37be9db613c2898645"

# URL of the file to transcribe
FILE_URL = "audio.wav"

# You can also transcribe a local file by passing in a file path
# FILE_URL = './path/to/file.mp3'

transcriber = aai.Transcriber()
transcript = transcriber.transcribe(FILE_URL)

print(transcript.text)
