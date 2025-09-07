import os
import base64
import requests

HF_API_URL = "https://api.huggingface.co/generate-image"

def edit_frame(frame_path, prompt, seed, mask_path=None):
    with open(frame_path, "rb") as f:
        img_data = f.read()
    payload = {
        "inputs": base64.b64encode(img_data).decode(),
        "parameters": {
            "model": "nano-banana",
            "prompt": prompt,
            "seed": seed,
            "guidance_scale": 9,
            "mask": None
        }
    }
    if mask_path:
        with open(mask_path,"rb") as m: payload["parameters"]["mask"] = base64.b64encode(m.read()).decode()
    resp = requests.post(HF_API_URL, json=payload, headers={"Authorization": f"Bearer {os.getenv('HF_TOKEN')}"})
    out_b64 = resp.json()["generated_image"]
    return base64.b64decode(out_b64)
