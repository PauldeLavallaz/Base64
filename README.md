# JSON → Image (base64 data URI) for ComfyUI

Custom node that reads a JSON payload like:
```json
{
  "images": [
    {
      "url": "data:image/png;base64,iVBORw0KGgo...",
      "content_type": "image/png",
      "file_name": "example.png",
      "file_size": 504205,
      "width": null,
      "height": null
    }
  ],
  "seed": 1999403483
}
```
and outputs an `IMAGE` tensor for ComfyUI.

## Installation

1. Download this repo or clone it into your ComfyUI custom nodes folder:
   - Path: `ComfyUI/custom_nodes/comfy-json-base64-image`
2. Restart ComfyUI.

## Usage

- Add the node **“JSON → Image (base64 data URI)”** from `utils/io`.
- Paste your JSON into `json_str` (the whole object).
- Optionally set `index` if `images` has multiple items.
- Output is a ComfyUI `IMAGE` tensor ready to connect to your pipeline.

## Notes
- Supports full data URIs (`data:image/png;base64,...`) and raw base64 strings (no prefix).
- Converts to RGB and normalizes to `[0,1]` as `1xHxWxC` tensor.
- No external dependencies beyond ComfyUI default stack (Pillow, NumPy, Torch).

## License
MIT
