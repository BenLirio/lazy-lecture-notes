import os
import openai
from pydub import AudioSegment
from pydub.utils import make_chunks

openai.api_key = os.getenv("OPENAI_API_KEY")
audio = AudioSegment.from_mp3("audio_stitch.mp3")

chunk_duration_minutes = 10
chunk_duration_seconds = chunk_duration_minutes * 60
chunk_duration_ms = chunk_duration_seconds * 1000

audio_chunks = make_chunks(audio, chunk_duration_ms)

previous_transcript = ""
with open("transcript.txt", "w") as transcript_file:
  for i, audio_chunk in enumerate(audio_chunks):
    chunk_filename = f"audio_chunk_{i}.mp3"
    audio_chunk.export(chunk_filename, format="mp3")
    with open(chunk_filename, "rb") as chunk_file:
      transcript = openai.Audio.transcribe(
        prompt=previous_transcript,
        model="whisper-1",
        file=chunk_file,
      ).text
      previous_transcript = transcript
      transcript_file.write(transcript)
    os.remove(chunk_filename)