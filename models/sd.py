import torch
from diffusers import DiffusionPipeline


def model_SD(prompt: str, torchDevice: str):
    model_id = "CompVis/stable-diffusion-v1-4"

    pipe = DiffusionPipeline.from_pretrained(
        model_id, torch_dtype=torch.float32)

    pipe = pipe.to(torchDevice)

    image = pipe(prompt).images[0]

    image.save("model_base.png")
