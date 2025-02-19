# execute_pair_workflow.py

## ComfyUI Workflow Executor

### Description
This script executes a generated ComfyUI workflow for image pair blending. It connects to a local ComfyUI server, queues the workflow, and monitors its execution progress.

### Usage
```bash
./execute_pair_workflow.py <workflow.json>
```

### Arguments
- `workflow.json` JSON workflow file to execute

### Dependencies
- Python 3.x
- requests
- websocket-client
- json

### Output
- Status updates during execution
- Generated image in ComfyUI output directory

### Example
```bash
./execute_pair_workflow.py workflow.json
```

*Author:* JW

*Last Updated:* 10-03-2023 16:00

---

