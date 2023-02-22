from datasets import load_dataset
from PIL import Image
from transformers import AutoProcessor, BlipForConditionalGeneration
import os

HUB_PATH = "polytechXhf/jojos-dataset"


def caption_dataset(image_path):
    """
        Captionning all images in the dataset (through metadata.jsonl)
    """

    if(os.path.exists(image_path)):

        processor = AutoProcessor.from_pretrained(
            "Salesforce/blip-image-captioning-base")
        model = BlipForConditionalGeneration.from_pretrained(
            "Salesforce/blip-image-captioning-base")

        image = Image.open(image_path)

        inputs = processor(
            images=image, padding="max_new_tokens", return_tensors="pt")

        output = model.generate(**inputs)

        return processor.decode(output[0], skip_special_tokens=True)


def export_dataset():
    """
        Create a Dataset from scrapped datas and push it on the hf-hub
    """
    print("Exporting dataset in progress...")

    jojo_dataset = load_dataset("imagefolder", data_dir="assets")

    jojo_dataset.push_to_hub(HUB_PATH)
    print("Dataset exported successfuly !")
