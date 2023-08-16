import os
import openai



def gptsummary(txt_file):
  with open(txt_file, 'r') as file:
    textfile = file.read()
  
  # Set your API key
  openai.api_key = os.environ['OPENAI_API_KEY']
  
  # Create a request to the ChatCompletion endpoint
  response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo-16k",
    messages=[
      {"role": "system",
      "content": "Summarize the provided content into a couple paragraphs"},
      {"role": "user",
       "content": textfile}
    ]
  )
  
  # Extract and print the assistant's text response
  print(response["choices"][0]["message"]["content"])
  summary = response["choices"][0]["message"]["content"]
  with open('gpt-summary.txt', 'w') as file:
    file.write(summary)

if __name__ == "__main__":
  txt_file = "transcript.txt" #input the txt file to summarize
  gptsummary(txt_file)