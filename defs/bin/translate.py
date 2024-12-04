#!/bin/env python3
import argparse
import requests
import nltk
from pathlib import Path
from pprint import pprint
import os
from openai import OpenAI

nltk.download('punkt')

def translate_text_ollama(text):
    system_prompt = f"""
# You are a native speaker of English and Castillano Spanish. You were raised in Buenos Aires Argentina so you are very familiar with the great authors such as Jorge Borges and others.
"""

    response = requests.post('http://localhost:11434/api/generate',
        json={
            "model": "llama3:8b",
            "prompt": f"""

{system_prompt}\n\n## Translate the following text to Castillano Spanish.
- Do not add any notes or commentary.
- Maintain the markdown formatting.
- Do not add additional new lines or carriage returns.


{text}
""",


            "stream": False
        })

    return response.json()['response']


def translate_text_openai(text):
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{
                "role": "system",
                "content": "You are a native speaker of English and Castillano Spanish, raised in Buenos Aires Argentina, familiar with authors like Jorge Borges."
            },
            {
                "role": "user",
                "content": f"Translate to Castillano Spanish, maintaining markdown formatting without added notes or line breaks:\n\n{text}"
            }]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"OpenAI API error: {e}")
        return text


def process_file(input_file):
    text = Path(input_file).read_text(encoding='utf-8')
    sentences = nltk.sent_tokenize(text)
    output_file = input_file.rsplit('.', 1)[0] + '_es.' + input_file.rsplit('.', 1)[1]
    print(f"Processing {input_file} -> {output_file}")

    lines = len(sentences)
    line = 0

    with open(output_file, 'w', encoding='utf-8') as f:
        for sentence in sentences:
            line += 1
            if line > 100:
                break
            print(f"{line}/{lines}          ", end='\r')
            # translated = translate_text_ollama(sentence.strip())
            translated = translate_text_openai(sentence.strip())
            f.write(translated + '\n')
            f.flush()
            print(translated)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', help='Input markdown file')
    args = parser.parse_args()
    process_file(args.input_file)

if __name__ == '__main__':
    main()