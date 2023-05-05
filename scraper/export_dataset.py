import time
from transformers import AutoProcessor, BlipForConditionalGeneration
from PIL import Image
from datasets import load_dataset
import torch
from tqdm import tqdm


def create_metadata_from_images(save_path: str, images_filename: list[str], images_name: list[str], precision: str):
    """
        Function that create the 'metadata.jsonl' file for Dataset from images informations
    """
    print("Dataset creation currently processing...")
    start_time = time.time()
    metadata_file = open(save_path + "/metadata.jsonl", "a")

    # BLIP caption generation
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    mini_batch = 16

    processor = AutoProcessor.from_pretrained(
        "Salesforce/blip-image-captioning-large")
    model = BlipForConditionalGeneration.from_pretrained(
        "Salesforce/blip-image-captioning-large", torch_dtype=torch.float16 if precision == "float16" else torch.float32).to(device).to(device)

    captions = []

    for i in tqdm(range(0, len(images_filename), mini_batch)):

        mini_batch_images = [Image.open(save_path + "/" + image_filename)
                             for image_filename in images_filename[i:i+mini_batch]]

        inputs = processor(
            images=mini_batch_images,  return_tensors="pt").to(device, torch.float16 if precision == "float16" else torch.float32)

        output = model.generate(
            **inputs, max_new_tokens=50)

        mini_batch_captions = processor.batch_decode(
            output, skip_special_tokens=True)

        captions.extend(mini_batch_captions)

    # 'metadata.jsonl' file creation
    print("'metadata.jsonl' file creation in progress...")
    for i in tqdm(range(0, len(captions))):
        data_input = """{"char_name": "%s", "file_name": "%s", "text": "%s"}\n""" % (
            images_name[i], images_filename[i], captions[i])

        metadata_file.write(data_input)

    print("[TIME] create_metadata_from_images(): %.5ss" %
          (time.time() - start_time))


def export_dataset(manga_scraped: str, hub_path: str):
    """
        Create a Dataset from scrapped datas and push it on the hf-hub
    """
    print("Exporting dataset in progress...")

    jojo_dataset = load_dataset(
        "imagefolder", data_dir=f"assets/train/{manga_scraped}", split="train")

    jojo_dataset.push_to_hub(hub_path)
    print("Dataset exported successfuly !")
