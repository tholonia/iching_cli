#!/bin/env python

"""
=============================================================================
execute_pair_workflow.py - ComfyUI Workflow Executor
=============================================================================

Description:
    This script executes a generated ComfyUI workflow for image pair blending.
    It connects to a local ComfyUI server, queues the workflow, and monitors
    its execution progress.

Usage:
    ./execute_pair_workflow.py <workflow.json>

Arguments:
    workflow.json       JSON workflow file to execute

Dependencies:
    - Python 3.x
    - requests
    - websocket-client
    - json

Output:
    - Status updates during execution
    - Generated image in ComfyUI output directory

Example:
    ./execute_pair_workflow.py workflow.json

Author: JW
Last Updated: 2024
=============================================================================
"""

import json
import requests
import websocket
import uuid
import sys
import os
from pathlib import Path

# ComfyUI server settings
SERVER_URL = "http://localhost:8188"
WS_URL = "ws://localhost:8188/ws"

def load_workflow(filename):
    """Load workflow from JSON file."""
    with open(filename, 'r') as f:
        return json.load(f)

def queue_prompt(workflow):
    """Queue workflow to ComfyUI server."""
    p = {
        "prompt": workflow,
        "client_id": str(uuid.uuid4())
    }
    response = requests.post(f"{SERVER_URL}/prompt", json=p)
    if response.status_code != 200:
        raise Exception(f"Failed to queue prompt: {response.status_code}")
    return response.json()

def main():
    # Check arguments
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <workflow.json>")
        sys.exit(1)

    workflow_file = sys.argv[1]
    if not os.path.exists(workflow_file):
        print(f"Error: Workflow file {workflow_file} not found")
        sys.exit(1)

    # Load workflow
    try:
        workflow = load_workflow(workflow_file)
    except Exception as e:
        print(f"Error loading workflow: {e}")
        sys.exit(1)

    # Connect to websocket
    ws = websocket.WebSocket()
    try:
        ws.connect(WS_URL)
    except Exception as e:
        print(f"Error connecting to ComfyUI server: {e}")
        sys.exit(1)

    # Queue workflow
    try:
        response = queue_prompt(workflow)
        prompt_id = response.get('prompt_id')
        print(f"Workflow queued with ID: {prompt_id}")
    except Exception as e:
        print(f"Error queuing workflow: {e}")
        sys.exit(1)

    # Monitor execution
    try:
        while True:
            message = ws.recv()
            if not message:
                continue

            data = json.loads(message)

            if data['type'] == 'execution_start':
                print("Execution started...")

            elif data['type'] == 'executing':
                node_id = data['data']['node']
                print(f"Executing node {node_id}...")

            elif data['type'] == 'progress':
                value = data['data']['value']
                max_value = data['data']['max']
                print(f"Progress: {value}/{max_value}")

            elif data['type'] == 'executed':
                node_id = data['data']['node']
                if 'output' in data['data']:
                    output = data['data']['output']
                    if 'images' in output:
                        for image in output['images']:
                            print(f"Generated image: {image['filename']}")

            elif data['type'] == 'execution_complete':
                print("Workflow completed successfully")
                break

    except KeyboardInterrupt:
        print("\nExecution interrupted by user")
    except Exception as e:
        print(f"Error during execution: {e}")
    finally:
        ws.close()

if __name__ == "__main__":
    main()