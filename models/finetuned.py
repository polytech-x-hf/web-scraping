import torch
from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler
from huggingface_hub import hf_hub_download


def dummy(images, **kwargs):
    return images, False


def model_finetuned(prompt: str, torchDevice: str):
    # model_base = "runwayml/stable-diffusion-v1-5"
    model_base = "CompVis/stable-diffusion-v1-4"

    pipe = StableDiffusionPipeline.from_pretrained(
        model_base, torch_dtype=torch.float32)
    pipe.scheduler = DPMSolverMultistepScheduler.from_config(
        pipe.scheduler.config)

    # pipe.enable_attention_slicing()

    model_path = hf_hub_download(
        repo_id="polytechXhf/stable-diffusion-jojo-adapter-100", filename="pytorch_lora_weights.bin", revision="main")

    # model_path = "/Users/yazid/Desktop/sd-onepiece-model-lora-4e-4-adam/checkpoint-10000/pytorch_model.bin"
    pipe.unet.load_attn_procs(model_path)
    pipe.to(torchDevice)

    pipe.safety_checker = dummy

    for i in range(3):
        image = pipe(prompt, num_inference_steps=25,
                     guidance_scale=7.5).images[0]
        image.save(f"model_finetuned_{i}.png")
