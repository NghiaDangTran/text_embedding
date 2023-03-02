import openai
import json
import textwrap
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv('API_KEY')

def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()




def gpt3_embedding(content, engine='text-similarity-ada-001'):
    response = openai.Embedding.create(input=content,engine=engine)
    vector = response['data'][0]['embedding']  # this is a normal list
    return vector


if __name__ == '__main__':
    alltext = open_file('input.txt')
    chunks = textwrap.wrap(alltext, 3000)
    result = list()
    for chunk in chunks:
        embedding = gpt3_embedding(chunk.encode(encoding='ASCII',errors='ignore').decode())
        info = {'content': chunk, 'vector': embedding}
        print(info, '\n\n\n')
        result.append(info)
    with open('index.json', 'w') as outfile:
        json.dump(result, outfile, indent=2)