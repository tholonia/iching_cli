#!/bin/env python
import os
import requests
import json
# Replace 'YOUR_API_KEY' with your actual xAI API key
api_key = os.getenv('GROK_API_KEY')
if api_key == 'YOUR_API_KEY':
    raise ValueError("Please set your GROK API key in the 'XAI_API_KEY' environment variable or replace 'YOUR_API_KEY'.")

# Define the endpoint URL
url = "https://api.x.ai/v1/models"

# Set up the headers with the API key
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# Define the prompt and other parameters
data = {
    'model': 'grok-beta',  # Specify the model you want to use
    'messages': [
        {'role': 'system', 'content': 'You are a helpful assistant.'},
        {'role': 'user', 'content': 'Hello, how can I use the Grok API?'}
    ],
    'temperature': 0.7  # Adjust the creativity of the response
}

try:
    # Make the GET request to fetch the models
    response = requests.get(url, headers=headers,data=json.dumps(data))
    response.raise_for_status()  # Raise an exception for HTTP errors

    # Parse the JSON response
    models = response.json().get('data', [])

    if not models:
        print("No models found.")
    else:
        print("Available models:")
        for model in models:
            print(f"- {model['id']}: Created on {model['created']}")
except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
