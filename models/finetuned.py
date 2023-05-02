import torch
from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler
from huggingface_hub import hf_hub_download


def model_finetuned(prompt: str, torchDevice: str):
    model_base = "CompVis/stable-diffusion-v1-4"

    pipe = StableDiffusionPipeline.from_pretrained(
        model_base, torch_dtype=torch.float32)
    pipe.scheduler = DPMSolverMultistepScheduler.from_config(
        pipe.scheduler.config)

    model_path = hf_hub_download(
        repo_id="polytechXhf/stable-diffusion-jojo-adapter-1", filename="pytorch_lora_weights.bin")

    pipe.unet.load_attn_procs(model_path)
    pipe.to("mps")

    image = pipe(prompt, num_inference_steps=25,
                 guidance_scale=7.5).images[0]
    image.save("model_finetuned.png")

