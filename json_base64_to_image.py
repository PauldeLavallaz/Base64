# json_base64_to_image.py
# ComfyUI custom node: JSON (images[0].url base64 data URI) -> IMAGE tensor

import json
import base64
from io import BytesIO
from PIL import Image
import numpy as np
import torch
import re

DATA_URI_RE = re.compile(r"^data:(?P<mime>[^;]+);base64,(?P<b64>.+)$", re.DOTALL)

def _to_image_tensor(pil_img: Image.Image) -> torch.Tensor:
    img = pil_img.convert("RGB")
    arr = np.array(img).astype(np.float32) / 255.0  # HWC, 0..1
    return torch.from_numpy(arr)[None, ...]  # 1xHxWxC

def _decode_data_uri(s: str) -> Image.Image:
    m = DATA_URI_RE.match(s.strip())
    if not m:
        # allow raw base64 without data: prefix
        b64 = s.strip()
    else:
        b64 = m.group("b64")
    try:
        data = base64.b64decode(b64, validate=False)
    except Exception as e:
        raise RuntimeError(f"No se pudo decodificar base64: {e}")
    try:
        return Image.open(BytesIO(data))
    except Exception as e:
        raise RuntimeError(f"No se pudo abrir la imagen: {e}")

class JSONBase64ToImage:
    """
    Recibe un JSON con el formato:
    {"images":[{"url":"data:image/png;base64,...","content_type":"image/png","file_name":"x.png","file_size":123,"width":null,"height":null}], "seed":123}
    Toma el índice indicado (por defecto 0), decodifica y devuelve IMAGE.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "json_str": ("STRING", {"multiline": True, "forceInput": True}),
            },
            "optional": {
                "index": ("INT", {"default": 0, "min": 0, "step": 1}),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "run"
    CATEGORY = "utils/io"
    OUTPUT_NODE = False

    def run(self, json_str: str, index: int = 0):
        try:
            payload = json.loads(json_str)
        except Exception as e:
            raise RuntimeError(f"JSON inválido: {e}")

        if not isinstance(payload, dict) or "images" not in payload:
            raise RuntimeError("JSON debe contener la clave 'images' (lista).")

        images = payload.get("images")
        if not isinstance(images, list) or len(images) == 0:
            raise RuntimeError("'images' debe ser una lista no vacía.")

        if index < 0 or index >= len(images):
            raise RuntimeError(f"Índice fuera de rango: {index} (len={len(images)}).")

        item = images[index]
        if not isinstance(item, dict) or "url" not in item:
            raise RuntimeError("Cada item en 'images' debe tener la clave 'url'.")

        pil = _decode_data_uri(str(item["url"]))
        tensor = _to_image_tensor(pil)
        return (tensor,)

# ----- ComfyUI registration -----
NODE_CLASS_MAPPINGS = {
    "JSONBase64ToImage": JSONBase64ToImage,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "JSONBase64ToImage": "JSON → Image (base64 data URI)",
}
