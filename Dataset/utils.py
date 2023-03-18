from datasets import load_dataset
from PIL import Image
from transformers import AutoProcessor, BlipForConditionalGeneration
import os

HUB_PATH = "polytechXhf/jojos-dataset"
HUB_PATH_TEST = "polytechXhf/jojos-dataset-small"


def caption_dataset(image_path):
    """
        Captionning all images in the dataset (through metadata.jsonl)
    """

    if(os.path.exists(image_path)):

        processor = AutoProcessor.from_pretrained(
            "Salesforce/blip-image-captioning-large")
        model = BlipForConditionalGeneration.from_pretrained(
            "Salesforce/blip-image-captioning-large").to("mps")

        image = Image.open(image_path)

        inputs = processor(
            images=image,  return_tensors="pt").to("mps")

        output = model.generate(
            **inputs, max_new_tokens=50)

        return processor.decode(output[0], skip_special_tokens=True)


def export_dataset(manga_scraped: str):
    """
        Create a Dataset from scrapped datas and push it on the hf-hub
    """
    print("Exporting dataset in progress...")

    jojo_dataset = load_dataset(
        "imagefolder", data_dir=f"assets/train/{manga_scraped}", split="train")

    jojo_dataset.push_to_hub(HUB_PATH_TEST)
    print("Dataset exported successfuly !")
