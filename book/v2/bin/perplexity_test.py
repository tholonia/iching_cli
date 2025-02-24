#!/bin/env python

import requests
import json
import os

# Replace with your Perplexity API key
api_key = os.getenv('PERPLEXITY_API_KEY')

# Define the API endpoint
url = 'https://api.perplexity.ai/chat/completions'

# Set up the headers with the API key
headers = {
    'Authorization': f'Bearer {api_key}',
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}

# Define the prompt and other parameters
data = {
    'model': 'sonar-reasoning-pro',  # Specify the model you want to use
    'messages': [
        {'role': 'system', 'content': 'You are a helpful assistant.'},
        {'role': 'user', 'content': 'Hello, how can I use the Perplexity API?'}
    ],
    'temperature': 0.7,  # Adjust the creativity of the response
    'max_tokens': 1024   # Maximum length of the response
}

# Send the POST request
response = requests.post(url, headers=headers, json=data)

# Check if the request was successful
if response.status_code == 200:
    result = response.json()
    # Extract and print the assistant's reply
    reply = result['choices'][0]['message']['content']
    print('Assistant:', reply)
else:
    print(f'Error: {response.status_code}')
    print(response.text)