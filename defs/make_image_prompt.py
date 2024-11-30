#!/bin/env python

import requests
import sys
import os
import json

# Make sure you have your OpenAI API key set as an environment variable.
API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    raise ValueError("Please set your OpenAI API key as an environment variable named OPENAI_API_KEY.")

# Ensure the correct number of command line arguments
if len(sys.argv) != 2:
    print("Usage: python script.py <filename>")
    sys.exit(1)

filename = sys.argv[1]

# Read the hexagram from the provided file
try:
    with open(filename, 'r') as file:
        hexagram_text = file.read()
except FileNotFoundError:
    print(f"Error: File '{filename}' not found.")
    sys.exit(1)

# Define the prompt
prompt = (
    "Describe an image that best portrays the meaning of the following I Ching hexagram.\n\n"
    "This description must be in the form of a prompt to be used to create an image in Stable DiffusionComfyUI.\n\n"
    "Select the most appropriate style for the image independent of the medium or artist, for example, Realism, Impressionism, Expressionism, Abstract, Cubism, Surrealism, Symbolism, Art Nouveau, Art Deco, Minimalism, Pop Art, Futurism, Gothic, Baroque, Neoclassicism, Romanticism, Fauvism, Bauhaus, Ink Wash, Typography Art, Collage, Pointillism, Stippling, Retro, Vintage, Fantasy Art, Op Art, Street Art, Graffiti, Geometric Abstraction, Contemporary Figurative, Conceptual Art, Fantasy Realism, Digital Art, Graffiti.\n\n"
    "Select the most appropriate medium independent of medium or artist, such as Graphite, Charcoal, Ink, Colored Pencils, Pastels, Markers, Watercolor, Gouache, Acrylic, Oil Paint, Pen and Wash, Linocut, Woodcut, Etching, Engraving, Lithography, Screen Printing, Monoprint, Giclée, Collage, Mixed Drawing Media, Digital Painting, Digital Illustration, Photography, Cyanotype, Typography, Stippling, Pointillism, Ink Wash, Gold Leaf.\n\n"
    "Select the artist who best exemplifies the image independent of style or medium.\n\n"
    "# I Ching Hexagram follows:\n\n"
    + hexagram_text
)

# Make the API call
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}

data = {
    "model": "gpt-3.5-turbo",
    "messages": [
        {"role": "user", "content": prompt}
    ],
    "max_tokens": 200,
    "temperature": 0.7
}

try:
    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers=headers,
        data=json.dumps(data)
    )
    response.raise_for_status()
    result = response.json()
    image_prompt = result["choices"][0]["message"]["content"].strip()

    # Save the response to "image_prompt.txt"
    with open('image_prompt.txt', 'w') as output_file:
        output_file.write(image_prompt)

    print("Image prompt has been saved to 'image_prompt.txt'.")
except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
    sys.exit(1)
