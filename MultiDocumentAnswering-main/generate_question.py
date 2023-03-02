import openai
import json
import numpy as np
import textwrap
import re
from time import time, sleep
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv('API_KEY')

def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()

def gpt3_completion(prompt, engine='text-davinci-003', temp=0.81, top_p=0.82, tokens=1000, freq_pen=0, pres_pen=0.0, stop=['<<END>>']):
    max_retry = 1
    retry = 0
    prompt = prompt.encode(encoding='utf-8', errors='ignore').decode()
    print(prompt)
    while True:
        try:
            response = openai.Completion.create(
                engine=engine,
                prompt=prompt,
                temperature=temp,
                max_tokens=tokens,
                top_p=top_p,
                frequency_penalty=freq_pen,
                presence_penalty=pres_pen,
                stop=stop)
            print(response)
            text = (response['choices'][0]['text']).encode(encoding='utf-8', errors='ignore').decode().strip()
            replaced_text = re.sub(r"^\d+\. ", "", text, flags=re.MULTILINE)

            
            # text = re.sub('\s+', ' ', text)


            filename = 'gpt3_questions_v2.txt'
            with open('questions/%s' % filename, 'a', encoding='utf-8') as outfile:

                outfile.write( replaced_text)
            return text
        except Exception as oops:
            retry += 1
            if retry >= max_retry:
                return "GPT3 error: %s" % oops
            print('Error communicating with OpenAI:', oops)
            sleep(1)





if __name__ == '__main__':
    with open('index.json', 'r') as infile:
        data = json.load(infile)
    print(len(data))
    sample_prompt=open_file("questions_prompt.txt")
    for i in data:
        prompt = sample_prompt.replace(
                '<<PASSAGE>>', i['content'])
        answer = gpt3_completion(prompt)
    print("done")


 