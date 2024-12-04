#!/usr/bin/env python3

import sys
import json
import requests
import time
from openai import OpenAI
from pathlib import Path
import random
import argparse
import base64
import os
from colorama import Fore, Style

MODEL="gpt-4o"

def load_json_file(id_num):
    """Load the JSON file based on the ID number."""
    filename = f"{id_num}.json"
    print(Fore.YELLOW + "\nLoading JSON file: " + filename + Style.RESET_ALL)
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(Fore.RED + f"Error: File {filename} not found." + Style.RESET_ALL)
        sys.exit(1)

def get_openai_analysis(json_data):
    """Get analysis from OpenAI API."""
    # print("\nConnecting to OpenAI API...")
    client = OpenAI()

    prompt = """
    Read the recently attached Json file and print in the following format:
    Based on the top 6 verbs, top 6 nouns that describe material objects, and the top 6 adverbs, which we'll call the 'inputdata', fill in the following template:
    - Name: [value for key 'name' all in uppercase]
    - Theme: [value of the key 'order8parent']
    - Subtheme: [value of key 'order8child']
    - Object: [based on the inputdata, choose an individual animal or object OR a group of animals or objects best represents this hexagram]
    - Style: [based on the inputdata, choose a visual artistic style that best represents this hexagram from this list: Cave paintings, Abstract, Realism, Impressionism, Surrealism, Expressionism, Cubism, Futurism, Minimalism, Baroque, Rococo, Gothic, Art Nouveau, Art Deco, Neoclassicism, Romanticism, Fauvism, Symbolism, Dadaism, Pop Art, Op Art, Photorealism, Conceptual Art, Constructivism, Suprematism, De Stijl, Regionalism, Social Realism, Outsider Art, Street Art, Graffiti, Digital Art, Postmodernism, Hyperrealism, Modernism, Abstract Expressionism, Brutalism, Cyberpunk, Renaissance, Ukiyo-e, Zen Art, Indigenous Art, Folk Art, Byzantine, Pre-Raphaelite, Academic Art, Contemporary Art]
    - Medium: [based on the inputdata, choose a visual artistic medium that best represents this hexagram from this list: Oil painting, watercolor, acrylic painting, gouache, tempera, ink, charcoal, pencil, pastel, colored pencil, graphite, chalk, crayon, pen and ink, marker, digital painting, digital illustration, collage, mosaic, stained glass, fresco, wood carving, stone carving, lithography, screen printing, block printing, photography, graffiti, street art]
    - Artist: [based on the inputdata, choose a visual artistic artist that best represents this hexagram from this list: Leonardo da Vinci, Michelangelo, Raphael, Vincent van Gogh, Pablo Picasso, Rembrandt van Rijn, Katsushika Hokusai, Utagawa Hiroshige, Frida Kahlo, Diego Rivera, Georgia O'Keeffe, Andy Warhol, Jackson Pollock, Albrecht Dürer, Henri Matisse, Gustav Klimt, Caravaggio, Sandro Botticelli, Ben Enwonwu, El Anatsui, Nam June Paik, Gu Kaizhi, Fan Kuan, Qi Baishi, Jean-Michel Basquiat, Ansel Adams,Henri Cartier-Bresson,Sebastião Salgado,Edward Weston,Walker Evans,Gordon Parks,Joel Sartore]
    - Quality: award winning, highly symbolic
    Do not add any explanatory or parenthetical text.
    """

    try:
        # print("Sending request to OpenAI...")
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": str(json_data)}
            ]
        )
        analysis = response.choices[0].message.content
        # print("\nReceived analysis from OpenAI:")
        print(Fore.GREEN + analysis + Style.RESET_ALL)
        return analysis
    except Exception as e:
        print(Fore.RED + f"Error with OpenAI API: {e}" + Style.RESET_ALL)
        sys.exit(1)

def load_tholonic_primer():
    """Load the tholonic primer content."""
    primer_path = "/home/jw/store/src/iching_cli/defs/tholonic_primer.md"
    try:
        with open(primer_path, 'r') as file:
            return file.read()
    except Exception as e:
        print(Fore.RED + f"Warning: Could not load tholonic primer: {e}" + Style.RESET_ALL)
        return None

def get_image_analysis(image_path, original_analysis):
    """Send the generated image to OpenAI for analysis."""
    # print("\nGetting image analysis from OpenAI...")
    client = OpenAI()

    # Load tholonic primer
    tholonic_context = load_tholonic_primer()
    if tholonic_context:
        pass
        # print("Loaded tholonic primer for context")
    else:
        print(Fore.RED + "Warning: Proceeding without tholonic primer" + Style.RESET_ALL)

    # Read the image file
    with open(image_path, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode('utf-8')

    try:
        # Prepare the context message
        system_message = {
            "role": "system",
            "content": f"""You are an expert in tholonic concepts and I Ching interpretation.
Here is the context about tholonic concepts to consider in your analysis:

{tholonic_context if tholonic_context else 'No additional context available'}"""
        }

        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                system_message,
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": f"""
Here is the original analysis:
{original_analysis}

Explain why the object, style, medium and artist was chosen to represent this hexagram. Use tholonic concepts where possible, Answer in a concise narrative form and keep the answer as short as possible, one paragraph, no more than 200 words.
"""
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=300
        )
        analysis = response.choices[0].message.content
        # print("\nImage Analysis from OpenAI:")
        print(Fore.YELLOW + "\n" + analysis + Style.RESET_ALL)
        return analysis
    except Exception as e:
        print(Fore.RED + f"Error getting image analysis from OpenAI: {e}" + Style.RESET_ALL)
        return None

def get_prompt_status(server_address, prompt_id):
    """Check the status of a prompt"""
    response = requests.get(f"{server_address}/history/{prompt_id}")
    return response.json()


def get_latest_png():
    """
    Get the most recent PNG file from the ComfyUI output directory.
    Returns the full path to the file or None if no PNG files are found.
    """
    import glob
    from pathlib import Path

    output_dir = "/home/jw/src/ComfyUI/output/"

    try:
        # Get list of all PNG files in the directory
        png_files = glob.glob(os.path.join(output_dir, "*.png"))

        if not png_files:
            print(Fore.RED + f"No PNG files found in {output_dir}" + Style.RESET_ALL)
            return None

        # Get the most recent file using creation time
        latest_png = max(png_files, key=os.path.getctime)

        # print(f"Found latest PNG: {latest_png}")
        return latest_png

    except Exception as e:
        print(Fore.RED + f"Error accessing directory {output_dir}: {e}" + Style.RESET_ALL)
        return None


def generate_image(prompt, id_num, cfg=7.2, denoise=0.7, steps=30, batch_size=1, random_seed=False):
    """Generate image using ComfyUI API."""
    # print("\n=== Starting Image Generation Process ===")

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
    # print(Fore.RED + f"\nUsing seed: {seed}" + Style.RESET_ALL)

    # print("\nPreparing ComfyUI workflow configuration...")
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
                "sampler_name": "dpmpp_2m_sde"
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
        # print("\nSending request to ComfyUI API...")
        # print(f"POST request to: {server_address}/prompt")
        response = requests.post(f"{server_address}/prompt", json={"prompt": workflow})
        # print(f"Response status code: {response.status_code}")

        if response.status_code == 200:
            prompt_id = response.json()['prompt_id']
            # print(f"\nPrompt ID received: {prompt_id}")
            # print("\nMonitoring generation progress...")

            while True:
                status = get_prompt_status(server_address, prompt_id)
                if prompt_id in status:
                    if 'outputs' in status[prompt_id]:
                        # print("\n✓ Image generation completed successfully!")
                        # print(f"Output data: {status[prompt_id]['outputs']}")

                        # Get the path of the latest generated image
                        image_path = get_latest_png()
                        image_name = os.path.basename(image_path)
                        if not image_path:
                            print(Fore.RED + "Error: Could not find generated image" + Style.RESET_ALL)
                            break

                        # Send the image to OpenAI for analysis
                        image_analysis = get_image_analysis(image_path, prompt)
                        if image_analysis:
                            # Save the analysis to a text file
                            analysis_path = f"{image_name}_analysis.txt"
                            with open(analysis_path, 'w') as f:
                                f.write(image_analysis)
                            print(Fore.GREEN + f"\nAnalysis saved to {analysis_path}" + Style.RESET_ALL)
                        break
                    elif 'error' in status[prompt_id]:
                        print(Fore.RED + f"\n✗ Error during generation: {status[prompt_id]['error']}" + Style.RESET_ALL)
                        break
                print(".", end="", flush=True)
                time.sleep(1.0)
        else:
            print(Fore.RED + "\n✗ Failed to queue prompt" + Style.RESET_ALL)
            # print("Response content:", response.json())

    except Exception as e:
        print(Fore.RED + f"\n✗ Error with ComfyUI API: {e}" + Style.RESET_ALL)
        # print("\nFull error details:")
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
        print(Fore.RED + "Error: Please provide a two-digit number" + Style.RESET_ALL)
        sys.exit(1)

    # print(f"\n=== Starting process for ID: {args.id_num} ===")
    # print(Fore.YELLOW + f"Parameters: CFG={args.cfg}, Denoise={args.denoise}, Steps={args.steps}, "   f"Batch Size={args.batch_size}, Random Seed={args.random_seed}" + Style.RESET_ALL)

    # Load JSON data
    json_data = load_json_file(args.id_num)

    # Get OpenAI analysis
    analysis = get_openai_analysis(json_data)

    # Generate image using the analysis as prompt
    generate_image(analysis, args.id_num, args.cfg, args.denoise, args.steps,
                  args.batch_size, args.random_seed)

    # print("\n=== Process Complete ===")

if __name__ == "__main__":
    main()