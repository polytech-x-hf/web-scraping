import torch
from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler
from huggingface_hub import hf_hub_download
import gradio as gr
from PIL import Image

image_res = None
visible_res = False


def StableDiffusion(prompt: str):
    model_id = "CompVis/stable-diffusion-v1-4"
    device = "mps"

    pipe = StableDiffusionPipeline.from_pretrained(
        model_id, torch_dtype=torch.float32)
    pipe = pipe.to(device)

    image = pipe(prompt).images[0]

    image.save("stableDiffusion14.png")
    print("StableDiffusion generated!")


def FineTune(prompt: str):
    model_base = "CompVis/stable-diffusion-v1-4"

    pipe = StableDiffusionPipeline.from_pretrained(
        model_base, torch_dtype=torch.float32)
    pipe.scheduler = DPMSolverMultistepScheduler.from_config(
        pipe.scheduler.config)

    model_path = hf_hub_download(
        repo_id="polytechXhf/stable-diffusion-jojo-adapter-100", filename="pytorch_lora_weights.bin", revision="main")

    pipe.unet.load_attn_procs(model_path)
    pipe.to("mps")

    image = pipe(prompt, num_inference_steps=25, guidance_scale=7.5).images[0]
    image.save("model_finetuned.png")
    print("Model finetuned generated!")


def display_image():
    # Charger l'image à partir du chemin spécifié
    image_path = "model_finetuned.png"
    image = Image.open(image_path)
    return image


def old_runGradio():
    with gr.Blocks() as demo:

        gr.Markdown("# Project : Polytech x HF 🤗")
        gr.Markdown(
            "Test our new model which is specialized in Jojo and One Piece style")
        gr.Markdown(
            "Watch your words and phrases turn into beautiful images on the themes of Jojo and One Piece !")

        with gr.Column():
            base_model_to_use = gr.Dropdown(label="Which base model would you like to use?", choices=[
                                            "version 1", "version 2", "version 3"], value="version 1", interactive=True)

        with gr.Row() as upload_your_concept:
            with gr.Column():
                thing_description = gr.Markdown(
                    "Give a short description of what image you want to create. Here is an example of result for the following description : 'A photo of an astronaut riding a horse on mars' :")
                # thing_image_example = gr.Pil("image.png")
                things_naming = gr.Markdown("Now it's your turn !")

        prompt = gr.Textbox(label="Type your prompt")
        result_image = gr.Pil(visible=False)
        generate_button = gr.Button("Generate Image")
        progress_bar = gr.Textbox(visible=False)
        generate_ongoing = gr.Markdown(
            "## Genarating is ongoing ⌛... You can close this tab if you like or just wait.", visible=False)

        def generate(prompt):
            generate_ongoing.update(visible=True)
            iface.show_loading()
            # StableDiffusion(prompt)
            # FineTune(prompt)
            # iface.update()

        generate_button.click(fn=generate, inputs=[
            prompt], outputs=result_image, queue=False)

        with gr.Row():
            with gr.Column():
                image_res = gr.Markdown("## Result :", visible=visible_res)
                if visible_res == True:
                    result_image = gr.Pil(
                        "model_finetuned.png", visible=visible_res)

        # Post-training UI
        completed_generation = gr.Markdown(
            '''# ✅ Generating completed.''', visible=False)

        iface = gr.Interface(fn=display_image, inputs=None, outputs="image")

    demo.launch(share=True, debug=True)


def generateImage(prompt):

    # StableDiffusion(prompt)
    FineTune(prompt)
    return Image.open("model_finetuned.png")


def runGradio():
    demo = gr.Interface(fn=generateImage, inputs="text", outputs="image")
    demo.launch()
