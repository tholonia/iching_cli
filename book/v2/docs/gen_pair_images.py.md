# gen_pair_images.py

## ComfyUI Image Pair Blending Workflow Generator

### Description
This script generates and optionally executes a ComfyUI workflow that blends two input images using a VAE-based latent space blending technique.

### Usage
```bash
./gen_pair_images.py <image1> <image2> [options]
```
Batch with:
```bash
cat ../includes/pairs.csv \
| awk -F "," '{printf "./gen_pair_images.py %02d.png %02d.png --prefix %02d --execute --queue\n", $2, $3, $1}' |tail -32 > x.sh
```

### Arguments
- **image1**: First input image filename
- **image2**: Second input image filename
- **--prefix PREFIX**: Prefix for output filename (default: p06)
- **--output OUTPUT**: Output JSON filename (default: workflow.json)
- **--server SERVER**: ComfyUI server URL (default: http://localhost:8188)
- **--execute**: Execute the workflow after generation
- **--queue**: Queue the workflow to ComfyUI server (deprecated, use --execute)

### Dependencies
- Python 3.x
- requests
- websocket-client
- uuid
- json
- argparse
- random

### Output
- JSON workflow file
- Generated image with specified prefix (when executed)

### Example
```bash
./gen_pair_images.py image1.png image2.png --prefix blend01 --execute
```

*Author: JW*

*Last Updated:* 10-30-2023 08:00

---

