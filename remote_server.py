import os
import io
import base64
import subprocess
import sys
from PIL import Image
from flask import Flask, request, jsonify
import torch
from diffusers import StableDiffusionImg2ImgPipeline
from torchvision import transforms
from peft import LoraConfig, get_peft_model

# ==========================================================
#  Server config
# ===========================================================
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(" Using device:", device)

app = Flask(__name__)

# =========================================================
#  Load Stable Diffusion Img2Img pipeline ONCE
# ===========================================================
pipe = StableDiffusionImg2ImgPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    torch_dtype=torch.float16 if device.type == "cuda" else torch.float32
).to(device)
pipe.enable_attention_slicing()

print("Base SD Img2Img pipeline loaded")

# =======================================================
# Path to your Hunyuan3D repo
# =========================================================
HUNYUAN3D_DIR = "Hunyuan3D-2-main"

# =====================================================
# Helper to decode base64
# ======================================================
def decode_base64_image(data_url):
    encoded = data_url.split(",", 1)[1]
    return base64.b64decode(encoded)

# ===========================================================
# /stylize: LoRA style transfer endpoint
# ======================================================
@app.route('/stylize', methods=['POST'])
def stylize_image():
    data = request.get_json()
    drawing_data = data.get('drawingData')
    style = data.get('style')

    print(f"Stylizing with style: {style}")

    
    lora_path = f"lora_models/lora_{style}.pt"

   
    pipe.unet = get_peft_model(pipe.unet, LoraConfig(
        r=4,
        lora_alpha=16,
        target_modules=["to_q", "to_k", "to_v", "to_out.0"],
        lora_dropout=0.1,
        bias="none"
    ))
    pipe.unet.load_state_dict(torch.load(lora_path, map_location=device), strict=False)
    pipe.unet.to(device).eval()

    input_image = Image.open(io.BytesIO(decode_base64_image(drawing_data))).convert("RGB").resize((512, 512))

    prompt = f"{style} art, vivid colors, same structure, clean lines, no extra objects, beautiful brush strokes, proper sketches"

    # Run Img2Img
    result = pipe(
        prompt=prompt,
        image=input_image,
        strength=0.7,         
        guidance_scale=8.0, 
        num_inference_steps=30
    ).images[0]

    # Encode to base64
    output_io = io.BytesIO()
    result.save(output_io, format="PNG")
    output_b64 = base64.b64encode(output_io.getvalue()).decode("utf-8")

    return jsonify({"styled_image": f"data:image/png;base64,{output_b64}"})

# ===========================================================
#  /convert: run Hunyuan3D shape gen
# =====================================================
@app.route('/convert', methods=['POST'])
def convert_3d():
    data = request.get_json()
    drawing_data = data.get('drawingData')

    input_filename = "temp_drawing.png"
    output_filename = "static/output_3d.glb"

    decoded = decode_base64_image(drawing_data)
    Image.open(io.BytesIO(decoded)).convert("RGB").save(
        os.path.join(HUNYUAN3D_DIR, input_filename)
    )

    env = os.environ.copy()
    env["PYTHONPATH"] = os.path.abspath(HUNYUAN3D_DIR)
    result = subprocess.run(
        [sys.executable, "examples/shape_gen.py",
         "--input", input_filename,
         "--output", output_filename],
        cwd=HUNYUAN3D_DIR,
        env=env,
        capture_output=True,
        text=True
    )

    print(result.stdout)
    print(result.stderr)

    if result.returncode != 0:
        return jsonify({"error": f"3D generation failed: {result.stderr}"})

    print(" 3D model ready:", output_filename)
    return jsonify({"message": "3D model ready!", "glb": output_filename})

# ==================================================
# Run server
# ===========================================================
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
