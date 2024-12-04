#!/usr/bin/env python3

import sys
import json
import requests
import time
from openai import OpenAI
from pathlib import Path
import random
import argparse

def load_json_file(id_num):
    """Load the JSON file based on the ID number."""
    filename = f"{id_num}.json"
    print(f"\nLoading JSON file: {filename}")
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: File {filename} not found.")
        sys.exit(1)

def get_openai_analysis(json_data):
    """Get analysis from OpenAI API."""
    print("\nConnecting to OpenAI API...")
    client = OpenAI()

    prompt = """
    Read the uploaded recently attached json file:
    Based on the top 6 verbs, top 6 nouns that describe material objects, and the top 6 adverbs, which we'll call the 'inoputdata', fill in the following template and output the result:

    - Name: [value for key 'name' all in uppercase]
    - Theme: [value of the key 'order8parent']
    - Subtheme: [value of key 'order8child']
    - Object: [based on the inputdata, choose an individual animal or object OR what group of animals or objects best represents this hexagram]
    - Style: [[based on the inputdata, choose an visual artistic style that best represents this hexagram.  Examples are  (but not limited to) : Cave paintings, Abstract, Realism, Impressionism, Surrealism, Expressionism, Cubism, Futurism, Minimalism, Baroque, Rococo, Gothic, Art Nouveau, Art Deco, Neoclassicism, Romanticism, Fauvism, Symbolism, Dadaism, Pop Art, Op Art, Photorealism, Conceptual Art, Constructivism, Suprematism, De Stijl, Regionalism, Social Realism, Outsider Art, Street Art, Graffiti, Digital Art, Postmodernism, Installation Art, Performance Art, Hyperrealism, Modernism, Abstract Expressionism, Land Art, Brutalism, Cyberpunk, Renaissance, Ukiyo-e, Zen Art, Indigenous Art, Folk Art, Byzantine, Pre-Raphaelite, Academic Art, Contemporary Art.]
    - Medium: [[based on the inputdata, choose a visual artistic medium that best represents this hexagram. Examples are  (but not limited to) : Oil painting, watercolor, acrylic painting, gouache, tempera, ink, charcoal, pencil, pastel, colored pencil, graphite, chalk, crayon, pen and ink, marker, digital painting, digital illustration, collage, mosaic, stained glass, fresco, sculpture, wood carving, stone carving, metalwork, ceramics, pottery, glassblowing, casting, bronze sculpture, clay modeling, marble carving, 3D printing, resin casting, plaster sculpture, sand sculpture, ice sculpture, textile art, embroidery, weaving, quilting, printmaking, etching, engraving, lithography, screen printing, block printing, photography, film, video art, installation art, performance art, mixed media, assemblage, kinetic art, land art, calligraphy, graffiti, street art, body art, tattooing.]
    - Artist: [[based on the inputdata, choose a visual artistic artist best represents this hexagram. Examples are  (but not limited to) ; Leonardo da Vinci, Michelangelo, Raphael, Vincent van Gogh, Pablo Picasso, Claude Monet, Rembrandt van Rijn, Katsushika Hokusai, Utagawa Hiroshige, Yayoi Kusama, Frida Kahlo, Diego Rivera, Georgia O'Keeffe, Andy Warhol, Jackson Pollock, Albrecht Dürer, Henri Matisse, Gustav Klimt, Caravaggio, Sandro Botticelli, Phidias, Polykleitos, Thutmose, Ife Sculptors, Ben Enwonwu, El Anatsui, Nam June Paik, Gu Kaizhi, Fan Kuan, Qi Baishi,  Jean-Michel Basquiat, Ansel Adams.
    Do not add any explanatory or parenthetical text.
    """

    try:
        print("Sending request to OpenAI...")
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": str(json_data)}
            ]
        )
        analysis = response.choices[0].message.content
        print("\nReceived analysis from OpenAI:")
        print(analysis)
        return analysis
    except Exception as e:
        print(f"Error with OpenAI API: {e}")
        sys.exit(1)

def get_prompt_status(server_address, prompt_id):
    """Check the status of a prompt"""
    response = requests.get(f"{server_address}/history/{prompt_id}")
    return response.json()

def generate_image(prompt, id_num, cfg=7.2, denoise=0.7, steps=30, batch_size=1, random_seed=False):
    """Generate image using ComfyUI API."""
    print("\n=== Starting Image Generation Process ===")

    server_address = "http://127.0.0.1:8188"
    negative_prompt = """
    Ugly, poor quality, low resolution, blurry, distorted, pixelated, grainy, overexposed,
    underexposed, artifacts, watermark, text, letters, words, symbols, signature, watermark,
    nudity, violence, blood, gore, offensive content, inappropriate content, creepy, uncanny,
    distorted anatomy, deformed faces, asymmetry, unnatural proportions, extra limbs,
    extra fingers, missing limbs, missing fingers, unrealistic lighting, over-saturated colors,
    unnatural colors, flat shading, poor composition, chaotic background, cluttered background,
    low detail, poorly drawn, amateurish, unprofessional, cartoonish (unless desired),
    wrong perspective, tilted horizon, poor framing, unbalanced, incorrect depth,
    exaggerated expressions, and overly stylized (unless specified)
    """

    # Generate random seed if requested
    seed = random.randint(1, 1000000000) if random_seed else 8566257
    print(f"\nUsing seed: {seed}")

    print("\nPreparing ComfyUI workflow configuration...")
    workflow = {
        "3": {
            "class_type": "CheckpointLoaderSimple",
            "inputs": {
                "ckpt_name": "15/freedomRedmond_v1.safetensors"
            }
        },
        "4": {
            "class_type": "EmptyLatentImage",
            "inputs": {
                "batch_size": batch_size,
                "height": 1280,
                "width": 1280
            }
        },
        "5": {
            "class_type": "CLIPTextEncode",
            "inputs": {
                "clip": ["3", 1],
                "text": prompt
            }
        },
        "6": {
            "class_type": "CLIPTextEncode",
            "inputs": {
                "clip": ["3", 1],
                "text": negative_prompt
            }
        },
        "7": {
            "class_type": "KSampler",
            "inputs": {
                "cfg": cfg,
                "denoise": denoise,
                "latent_image": ["4", 0],
                "model": ["3", 0],
                "negative": ["6", 0],
                "positive": ["5", 0],
                "scheduler": "karras",
                "seed": seed,
                "steps": steps,
                "sampler_name": "euler_ancestral"
            }
        },
        "8": {
            "class_type": "VAEDecode",
            "inputs": {
                "samples": ["7", 0],
                "vae": ["3", 2]
            }
        },
        "9": {
            "class_type": "SaveImage",
            "inputs": {
                "filename_prefix": id_num,
                "images": ["8", 0]
            }
        }
    }

    try:
        print("\nSending request to ComfyUI API...")
        print(f"POST request to: {server_address}/prompt")
        response = requests.post(f"{server_address}/prompt", json={"prompt": workflow})
        print(f"Response status code: {response.status_code}")

        if response.status_code == 200:
            prompt_id = response.json()['prompt_id']
            print(f"\nPrompt ID received: {prompt_id}")
            print("\nMonitoring generation progress...")

            while True:
                status = get_prompt_status(server_address, prompt_id)
                if prompt_id in status:
                    if 'outputs' in status[prompt_id]:
                        print("\n✓ Image generation completed successfully!")
                        print(f"Output data: {status[prompt_id]['outputs']}")
                        break
                    elif 'error' in status[prompt_id]:
                        print(f"\n✗ Error during generation: {status[prompt_id]['error']}")
                        break
                print(".", end="", flush=True)
                time.sleep(1.0)
        else:
            print("\n✗ Failed to queue prompt")
            print("Response content:", response.json())

    except Exception as e:
        print(f"\n✗ Error with ComfyUI API: {e}")
        print("\nFull error details:")
        import traceback
        traceback.print_exc()

def main():
    parser = argparse.ArgumentParser(description='Generate images based on JSON analysis')
    parser.add_argument('id_num', help='Two-digit ID number')
    parser.add_argument('--cfg', type=float, default=7.2, help='CFG value (default: 7.2)')
    parser.add_argument('--denoise', type=float, default=0.7, help='Denoise value (default: 0.7)')
    parser.add_argument('--steps', type=int, default=30, help='Number of steps (default: 30)')
    parser.add_argument('--batch-size', type=int, default=1, help='Batch size (default: 1)')
    parser.add_argument('--random-seed', action='store_true', help='Use random seed instead of default')

    args = parser.parse_args()

    # Validate ID format
    if not (len(args.id_num) == 2 and args.id_num.isdigit()):
        print("Error: Please provide a two-digit number")
        sys.exit(1)

    print(f"\n=== Starting process for ID: {args.id_num} ===")
    print(f"Parameters: CFG={args.cfg}, Denoise={args.denoise}, Steps={args.steps}, "
          f"Batch Size={args.batch_size}, Random Seed={args.random_seed}")

    # Load JSON data
    json_data = load_json_file(args.id_num)

    # Get OpenAI analysis
    analysis = get_openai_analysis(json_data)

    # Generate image using the analysis as prompt
    generate_image(analysis, args.id_num, args.cfg, args.denoise, args.steps,
                  args.batch_size, args.random_seed)

    print("\n=== Process Complete ===")

if __name__ == "__main__":
    main()