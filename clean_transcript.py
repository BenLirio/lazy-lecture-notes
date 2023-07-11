import os
import openai
openai.api_key = os.getenv("OPENAI_API_KEY")


with open('transcript.txt') as f:
  transcript = f.read()

chunk_size = 8000
lecture_chunks = []
for i in range(0, len(transcript), chunk_size):
  lecture_chunks.append(transcript[i:i+chunk_size])

# system = """
# Your goal is to convert a raw transcript of a lecture into a readable 
# You are CleanTranscriberBot, an agent that takes as input a word for word transcript of a lecture and outputs a cleaned up version of the transcript.
# Make sure to organize the transcript into proper paragraphs and use bullet points when needed.
# Feel free to make large edits, but you are NOT trying to summarize the lecture, instead you are trying to make the transcript more readable.
# For practical purposes, I can only provide you with a chunk of the lecture transcript at a time.
# Because of this, I will provide you with the last few sentances of the previous cleaned up lecture transcript for you to reference.
# Make sure to respond with only the cleaned up lecture transcript and no preamble.
# """
# system = """
# Your goal is to extract all of the technical terms and definitions from a lecture transcript.
# I will provide you with a section of the lecture transcript and you will respond with a list of all the technical terms and definitions.
# Make sure to only include the technical terms and definitions and no preamble.
# """
system = """
Your goal is to create an outline of a lecture given a lecture transcript.
I will provide you with a current outline (possibly empty) and a section of the lecture transcript.
Your task is to update the current outline with the new section of the lecture transcript.
This means that you may need to add or remove previous sections of the outline.
"""

# previous_lecture_notes = ""
def blockify(text):
  return f"\n\"\"\"\n{text}\n\"\"\"\n"
lecture_outline = ""
with open("cleaned_transcript.txt", "w") as lecture_notes_file:
  for i, lecture_chunk in enumerate(lecture_chunks):
    user = ""
    user += f"Outline: {blockify(lecture_outline)}"
    user += f"Transcript: {blockify(lecture_chunk)}"
    completion = openai.ChatCompletion.create(
      model="gpt-3.5-turbo-16k",
      messages=[
        {"role": "system", "content": system },
        {"role": "user", "content": user }
      ]
    )
    lecture_outline = completion.choices[0].message.content
  lecture_notes_file.write(lecture_outline)