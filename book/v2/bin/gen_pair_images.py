#!/bin/env python

"""
=============================================================================
gen_pair_images.py - ComfyUI Image Pair Blending Workflow Generator
=============================================================================

Description:
    This script generates and optionally executes a ComfyUI workflow that
    blends two input images using a VAE-based latent space blending technique.

Usage:
    ./gen_pair_images.py <image1> <image2> [options]

    batch with:
    cat ../includes/pairs.csv \
    | awk -F "," '{printf "./gen_pair_images.py %02d.png %02d.png --prefix %02d --execute --queue\n", $2, $3, $1}' |tail -32 > x.sh


Arguments:
    image1              First input image filename
    image2              Second input image filename
    --prefix PREFIX     Prefix for output filename (default: p06)
    --output OUTPUT     Output JSON filename (default: workflow.json)
    --server SERVER     ComfyUI server URL (default: http://localhost:8188)
    --execute          Execute the workflow after generation
    --queue            Queue the workflow to ComfyUI server (deprecated, use --execute)

Dependencies:
    - Python 3.x
    - requests
    - websocket-client
    - uuid
    - json
    - argparse
    - random

Output:
    - JSON workflow file
    - Generated image with specified prefix (when executed)

Example:
    ./gen_pair_images.py image1.png image2.png --prefix blend01 --execute

Author: JW
Last Updated: 2024
=============================================================================
"""

import json
import argparse
import requests
import websocket
import uuid
import sys
import time
import random

def create_workflow(image1, image2, prefix="X", image_prompt=""):
    # Generate a random seed
    seed = random.randint(1, 1000000000000000)

    workflow = {
        "1": {
            "inputs": {
                "image": image1,
                "upload": "image"
            },
            "class_type": "LoadImage",
            "_meta": {
                "title": "Load Image"
            }
        },
        "2": {
            "inputs": {
                "image": image2,
                "upload": "image"
            },
            "class_type": "LoadImage",
            "_meta": {
                "title": "Load Image"
            }
        },
        "13": {
            "inputs": {
                "vae_name": "sdxl_vae.safetensors"
            },
            "class_type": "VAELoader",
            "_meta": {
                "title": "Load VAE"
            }
        },
        "3": {
            "inputs": {
                "pixels": [
                    "1",
                    0
                ],
                "vae": [
                    "13",
                    0
                ]
            },
            "class_type": "VAEEncode",
            "_meta": {
                "title": "VAE Encode"
            }
        },
        "4": {
            "inputs": {
                "pixels": [
                    "2",
                    0
                ],
                "vae": [
                    "13",
                    0
                ]
            },
            "class_type": "VAEEncode",
            "_meta": {
                "title": "VAE Encode"
            }
        },
        "5": {
            "inputs": {
                "blend_factor": 0.5,
                "samples1": [
                    "3",
                    0
                ],
                "samples2": [
                    "4",
                    0
                ]
            },
            "class_type": "LatentBlend",
            "_meta": {
                "title": "Latent Blend"
            }
        },
        "6": {
            "inputs": {
                "seed": seed,
                "steps": 50,
                "cfg": 8,
                "sampler_name": "dpmpp_2m",
                "scheduler": "normal",
                "denoise": 0.32,
                "model": [
                    "7",
                    0
                ],
                "positive": [
                    "8",
                    0
                ],
                "negative": [
                    "9",
                    0
                ],
                "latent_image": [
                    "5",
                    0
                ]
            },
            "class_type": "KSampler",
            "_meta": {
                "title": "KSampler"
            }
        },
        "7": {
            "inputs": {
                "ckpt_name": "XL/RealitiesEdgeXLLIGHTNING_TURBOV7.safetensors"
            },
            "class_type": "CheckpointLoaderSimple",
            "_meta": {
                "title": "Load Checkpoint"
            }
        },
        "8": {
            "inputs": {
                "text": f"{image_prompt}. Choose a style that is most appropriate for the content. Hi-def, 8k, detailed, hyper-detailed, etc. Realistic, surreal, abstract, etc.",
                "clip": [
                    "7",
                    1
                ]
            },
            "class_type": "CLIPTextEncode",
            "_meta": {
                "title": "CLIP Text Encode (Prompt)"
            }
        },
        "9": {
            "inputs": {
                "text": "blur, noise, distortion, unnatural edges, glitch, artifacts, oversaturation, blurry details, unrealistic lighting",
                "clip": [
                    "7",
                    1
                ]
            },
            "class_type": "CLIPTextEncode",
            "_meta": {
                "title": "CLIP Text Encode (Prompt)"
            }
        },
        "10": {
            "inputs": {
                "filename_prefix": prefix,
                "images": [
                    "12",
                    0
                ]
            },
            "class_type": "SaveImage",
            "_meta": {
                "title": "Save Image"
            }
        },
        "12": {
            "inputs": {
                "samples": [
                    "6",
                    0
                ],
                "vae": [
                    "13",
                    0
                ]
            },
            "class_type": "VAEDecode",
            "_meta": {
                "title": "VAE Decode"
            }
        }
    }
    return workflow

def queue_prompt(server_url, workflow):
    """Queue workflow to ComfyUI server."""
    print("\n=== Queueing Workflow ===")
    print(f"Connecting to server: {server_url}")

    try:
        p = {
            "prompt": workflow,
            "client_id": str(uuid.uuid4())
        }
        response = requests.post(f"{server_url}/prompt", json=p)

        if response.status_code != 200:
            raise Exception(f"Failed to queue prompt: {response.status_code}")

        prompt_id = response.json().get('prompt_id')
        print(f"✓ Successfully queued workflow (ID: {prompt_id})")
        print(f"✓ Output will be saved to: /home/jw/ComfyUI/output/")
        return response.json()

    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to ComfyUI server. Is it running?")
        raise
    except Exception as e:
        print(f"❌ Error queueing workflow: {str(e)}")
        raise

def get_pairpath_info(hex_num):
    """Load JSON file and extract pairpath info."""
    hex_str = f"{int(hex_num):02d}"  # Zero-pad to 2 digits
    filepath = f"../regen/{hex_str}.json"

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

            # Get basic pairpath info
            pairpath = data['pairpath']

            # Find path_num from pathnum list if not in pairpath
            if 'path_num' not in pairpath:
                for path in pathnum:
                    if hex_num in [path[0], path[1]]:
                        pairpath['path_num'] = path[2]
                        break

            return {
                'image_prompt': pairpath['image_prompt'],
                'title': pairpath['title'],
                'path_num': pairpath.get('path_num', 0)  # Default to 0 if not found
            }

    except FileNotFoundError:
        print(f"Error: File {filepath} not found")
        sys.exit(1)
    except KeyError as e:
        print(f"Error: Missing key in {filepath}: {e}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in {filepath}")
        sys.exit(1)

def main():
    print("\n=== ComfyUI Image Pair Blending Workflow ===")

    parser = argparse.ArgumentParser(description='Generate and queue ComfyUI workflow')
    parser.add_argument('image1', help='First input image filename')
    parser.add_argument('image2', help='Second input image filename')
    parser.add_argument('--prefix', default='p06', help='Prefix for output filename')
    parser.add_argument('--output', default='workflow.json', help='Output JSON filename')
    parser.add_argument('--server', default='http://localhost:8188', help='ComfyUI server URL')
    parser.add_argument('--execute', action='store_true', help='Queue the workflow for execution')
    parser.add_argument('--queue', action='store_true', help='Queue the workflow (deprecated, use --execute)')
    args = parser.parse_args()

    # Extract hexagram number from image1 filename (assuming format NN.png)
    hex_num = int(args.image1.split('.')[0])

    # Get pairpath info
    pairpath_info = get_pairpath_info(hex_num)
    print(f"\n=== Pair Path Info ===")

    # Format title with path number at front and underscores
    title = f"p{pairpath_info['path_num']:02d}_{pairpath_info['title'].replace(' ', '_')}"
    print(f"Title: {title}")
    print(f"Image Prompt: {pairpath_info['image_prompt']}")

    # Create workflow filename using prefix
    workflow_file = f"{args.prefix}_workflow.json"

    print("\n=== Input Parameters ===")
    print(f"Image 1: {args.image1}")
    print(f"Image 2: {args.image2}")
    print(f"Path Number: {pairpath_info['path_num']}")
    print(f"Title: {pairpath_info['title']}")
    # print(f"Output prefix: {args.prefix}")
    # print(f"Workflow file: {workflow_file}")
    # print(f"Server URL: {args.server}")

    # Generate the workflow
    print("\n=== Generating Workflow ===")
    workflow = create_workflow(args.image1, args.image2, title, pairpath_info['image_prompt'])
    print("✓ Workflow structure created")
    print(f"✓ Output prefix set to: {args.prefix}")

    # Save the workflow to a file
    print(f"\n=== Saving Workflow ===")
    with open(workflow_file, 'w') as f:
        json.dump(workflow, f, indent=2)
    print(f"✓ Workflow saved to: {workflow_file}")

    # Queue if requested
    if args.execute or args.queue:
        try:
            queue_prompt(args.server, workflow)
            print("\n✓ Check ComfyUI interface for progress")
            print("Waiting 10 seconds before exit...")
            time.sleep(10)
            print("Done.")
        except Exception as e:
            print(f"❌ Failed to queue workflow: {str(e)}")
            sys.exit(1)

if __name__ == "__main__":
    main()