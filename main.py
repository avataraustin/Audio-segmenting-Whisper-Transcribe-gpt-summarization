import openai
import os
import sys
from pydub import AudioSegment
import math
from quarter import split_audio
from summary import gptsummary
import time

"""
This program processes an mp3 audio file and splits it into quarters. It requires FFMPEG. It then processes these chunks via OpenAi Whisper speech to text and creates an appended text file called transcript.txt and then it uses Openai GPT-3.5-turbo-16k to summarize the text into a few paragraphs when done. The user is required to fill in the starting mp3 audio file as the Audio_file_to_process variable below before running this program. Also be sure to configure your OpenAi API key in the Secrets before use. Too large of mp3 files may still max out RAM and produce an error unless system resources are boosted. Delete the transcript.txt file before use.
"""

####### Start here: ########
# USER MUST INPUT MP3 FILE NAME TO PROCESS INTO QUOTES BELOW:
Audio_file_to_process = "training-cb1.mp3"

# USER SHOULD EDIT THIS GUIDING PROMPT FOR DETERMINING SPELLING etc. for 
# THE WORDING OF THE TRANSCRIPTION
prompt_guide = "audio is the Iowa Ag Podcast with host, Peter Jaques"
###### End inputs.  Run program if ready #########



# This imported function splits the beginning audio into 4ths
# first param is mp3 file to split into quarters and save
# into the segmented folder. 2nd param is folder to save to.
split_audio(Audio_file_to_process, "segmented") 

time.sleep(10)

#OpenAi limit on uploaded mp3 file is 25 mb

try:
  openai.api_key = os.environ['OPENAI_API_KEY']
except KeyError:
  sys.stderr.write("""
  You need to set up your API key yet.
  Manage API keys at:
  https://platform.openai.com/signup

  Open the Secrets Tool and add OPENAI_API_KEY as a secret.
  """)
  exit(1)

# Get a list of all files in the folder
file_list = os.listdir("segmented")

# delete old transcript.txt file if it exists
if os.path.exists("transcript.txt"):
  os.remove("transcript.txt")

#create the transcript file and append whisper results
for file_name in file_list:
  # Upload your own mp3 file using the Files menu on the sidebar.
  audio_file = open("segmented/"+file_name, "rb")
  transcript = openai.Audio.transcribe("whisper-1", audio_file, prompt = prompt_guide)
  transcript_file = open("transcript.txt", "a")
  print("The transcript of the audio file is:\n\n")
  print(transcript["text"])
  print("\n\nTranscript saved to the file transcript.txt")
  transcript_file.write(transcript["text"])
  transcript_file.close()

time.sleep(10)

gptsummary("transcript.txt")

