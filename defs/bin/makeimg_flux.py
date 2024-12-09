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
from pprint import pprint

MODEL="gpt-4o"
N=os.environ['N']

def load_json_file(id_num):
    """Load the JSON file based on the ID number."""
    filename = f"/home/jw/src/iching_cli/defs/final/{id_num}.json"
    print(Fore.YELLOW + "\nLoading JSON file: " + filename + Style.RESET_ALL)
    try:
        with open(filename, 'r') as file:
            prejson =  json.load(file)
            #! Clear the image_description field
            prejson['hx']['core']['image_description'] = ""
            prejson['hx']['core']['image'] = ""
            # pprint(prejson)
            # input()
            return prejson
    except FileNotFoundError:
        print(Fore.RED + f"Error: File {filename} not found." + Style.RESET_ALL)
        sys.exit(1)

def get_openai_analysis(json_data,id_num):
    """Get analysis from OpenAI API and generate image prompt for ComfyUI."""

    print(Fore.WHITE + f"\nConnecting to OpenAI API..." + Style.RESET_ALL)
    client = OpenAI()

    #! Load prompt from prompt.md file.  Thsi is the prompt tha create a ComfyUI porompt
    with open(f"/home/jw/src/iching_cli/defs/final/s{N}/prompt.md", 'r') as file:
        prompt = file.read()


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
        print(Fore.WHITE + "\nGenerated prompt:" + Style.RESET_ALL)
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

Explain why the subject, style, and medium were chosen to represent this hexagram. Use tholonic concepts where possible, but avoid using the world 'tholon' or 'tholonic'. Answer in a concise narrative form and keep the answer as short as possible, one paragraph, no more than 200 words. Do not use any artists names.
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
        print(Fore.WHITE + "\nImage Analysis from OpenAI:" + Style.RESET_ALL)
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


def generate_image(prompt, args): #cfg=7.2, denoise=0.7, steps=30, batch_size=1, random_seed=False, ckpt="15/freedomRedmond_v1.safetensors"):
    """Generate image using ComfyUI API."""
    print(Fore.WHITE + f"Image {args.id_num}.png Generation Process" + Style.RESET_ALL)

    server_address = "http://127.0.0.1:8188"
    negative_prompt = ""

    # Generate random seed if requested
    seed = random.randint(1, 1000000000) if args.random_seed else 8566257
    # print(Fore.RED + f"\nUsing seed: {seed}" + Style.RESET_ALL)

    # print("\nPreparing ComfyUI workflow configuration...")



        # "4": {
        #     "class_type": "EmptyLatentImage",
        #     "inputs": {
        #         "batch_size": batch_size,
        #         "height": 1280,
        #         "width": 1280
        #     }



    workflow = {
  "6": {
    "inputs": {
      "text": prompt,
      "clip": [
        "30",
        1
      ]
    },
    "class_type": "CLIPTextEncode",
    "_meta": {
      "title": "CLIP Text Encode (Positive Prompt)"
    }
  },
  "8": {
    "inputs": {
      "samples": [
        "31",
        0
      ],
      "vae": [
        "30",
        2
      ]
    },
    "class_type": "VAEDecode",
    "_meta": {
      "title": "VAE Decode"
    }
  },
  "9": {
    "inputs": {
      "filename_prefix": args.id_num,
      "images": [
        "8",
        0
      ]
    },
    "class_type": "SaveImage",
    "_meta": {
      "title": "Save Image"
    }
  },
  "27": {
    "inputs": {
      "width": args.width,
      "height": args.height,
      "batch_size": args.batch_size
    },
    "class_type": "EmptySD3LatentImage",
    "_meta": {
      "title": "EmptySD3LatentImage"
    }
  },
  "30": {
    "inputs": {
      "ckpt_name": args.ckpt
    },
    "class_type": "CheckpointLoaderSimple",
    "_meta": {
      "title": "Load Checkpoint"
    }
  },
  "31": {
    "inputs": {
      "seed": seed,
      "steps": args.steps,
      "cfg": 1,
      "sampler_name": args.sampler,
      "scheduler": args.scheduler,
      "denoise": 1,
      "model": [
        "30",
        0
      ],
      "positive": [
        "35",
        0
      ],
      "negative": [
        "33",
        0
      ],
      "latent_image": [
        "27",
        0
      ]
    },
    "class_type": "KSampler",
    "_meta": {
      "title": "KSampler"
    }
  },
  "33": {
    "inputs": {
      "text": "",
      "clip": [
        "30",
        1
      ]
    },
    "class_type": "CLIPTextEncode",
    "_meta": {
      "title": "CLIP Text Encode (Negative Prompt)"
    }
  },
  "35": {
    "inputs": {
      "guidance": args.guidance,
      "conditioning": [
        "6",
        0
      ]
    },
    "class_type": "FluxGuidance",
    "_meta": {
      "title": "FluxGuidance"
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
    parser.add_argument('--random-seed',action='store_true', help='Use random seed instead of default')

    parser.add_argument('--cfg',        type=float, default=7.2,                            help='CFG value (default: 7.2)')
    parser.add_argument('--denoise',    type=float, default=0.7,                            help='Denoise value (default: 0.7)')
    parser.add_argument('--steps',      type=int,   default=30,                             help='Number of steps (default: 30)')
    parser.add_argument('--batch-size', type=int,   default=1,                              help='Batch size (default: 1)')
    parser.add_argument('--ckpt',       type=str,   default="15/flux1-dev-fp8.safetensors", help='Checkpoint to use (default: 15/flux1-dev-fp8.safetensors)')
    parser.add_argument('--guidance',   type=float, default=3.5,                            help='Guidance value (default: 3.5)')
    parser.add_argument('--sampler',    type=str,   default="euler",                        help='Sampler (default: euler)')
    parser.add_argument('--scheduler',  type=str,   default="simple",                       help='Scheduler (default: simple)')
    parser.add_argument('--width',      type=int,   default=1296,                           help='Width (default: 1296)')
    parser.add_argument('--height',     type=int,   default=960,                            help='Height (default: 960)')

    args = parser.parse_args()

    if args.ckpt:
        ckpt = args.ckpt
    else:
        ckpt = "15/freedomRedmond_v1.safetensors"


    # Validate ID format
    if not (len(args.id_num) == 2 and args.id_num.isdigit()):
        print(Fore.RED + "Error: Please provide a two-digit number" + Style.RESET_ALL)
        sys.exit(1)

    # print(f"\n=== Starting process for ID: {args.id_num} ===")
    # print(Fore.YELLOW + f"Parameters: CFG={args.cfg}, Denoise={args.denoise}, Steps={args.steps}, "   f"Batch Size={args.batch_size}, Random Seed={args.random_seed}" + Style.RESET_ALL)

    # Load JSON data
    json_data = load_json_file(args.id_num)

    # Get OpenAI analysis

    print(Fore.WHITE + f"Getting OpenAI analysis for {args.id_num}" + Style.RESET_ALL)


    comfyui_prompt = get_openai_analysis(json_data,args.id_num)


    # input()

    # Generate image using the analysis as prompt
    print(Fore.WHITE + f"Getting OpenAI Image" + Style.RESET_ALL)
    generate_image(comfyui_prompt,args)
    #     args.id_num,
    #     args.cfg,
    #     args.denoise,
    #     args.steps,
    #     args.batch_size,
    #     args.random_seed,
    #     argsckpt,
    #     args.guidance
    # )

    # print("\n=== Process Complete ===")

if __name__ == "__main__":
    main()