import os
import openai
import time

# Set your API key
openai.api_key = os.environ['OPENAI_API_KEY']

def gpt_chat_completion_xl(instructions: str, txt_body:str ):
  '''
  instructions: str, short system instruction to apply to txt_body
  txt_body: str, main text to process using instructions given
  '''
  response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo-16k",
    messages=[
      {"role": "system",
      "content": instructions},
      {"role": "user",
       "content": txt_body}
    ]
  )
  print(response["choices"][0]["message"]["content"])
  return response["choices"][0]["message"]["content"]

def gptsummary(txt_file):
  '''
  process transcript file into summary. uses gpt_chat_completion() to send the openai chat request. If full file fails, splits into seperate summarizations and combines.
  '''
  with open(txt_file, 'r') as file:
    textfile = file.read()
  

  # attempt to summarize entire transcript (16k or less tokens)
  try:
    summary = gpt_chat_completion_xl("Summarize the provided content into a couple paragraphs, use 'they' to refer to the speaker", textfile)
    
    with open('gpt-summary.txt', 'w') as sum_file:
      sum_file.write(summary)
  except:
    print('transcript too long, splitting summaries...\n')
    # split txt in half for batch processing
    num_chars = int(len(textfile) * .50)
    first_half_txt = textfile[:num_chars]
    second_half_txt = textfile[num_chars:]

    summary_one = gpt_chat_completion_xl("summarize the provided content while preserving all the main points, use 'they' to refer to the speaker", first_half_txt)
    time.sleep(10)

    summary_two = gpt_chat_completion_xl("summarize the provided content while preserving all the main points, use 'they' to refer to the speaker", second_half_txt)
    time.sleep(10)

    # delete any pre-existing gpt-summary txt file 
    if os.path.exists('gpt-summary.txt'):
      os.remove('gpt-summary.txt')

    # combine the seperate main point summaries
    concat_summary = summary_one + summary_two

    final_concat_summ = gpt_chat_completion_xl("Summarize or join the provided content into a couple of paragraphs", concat_summary)

    with open('gpt-summary.txt', 'a') as sum_file:
      sum_file.write(final_concat_summ)
      
      
    

if __name__ == "__main__":
  txt_file = "transcript.txt" #input the txt file to summarize
  gptsummary(txt_file)