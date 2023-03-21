import time
from transformers import AutoProcessor, BlipForConditionalGeneration
from PIL import Image
from datasets import load_dataset


def create_metadata_from_images(save_path: str, images_filename: list[str], images_name: list[str]):
    """
        Function that create the 'metadata.jsonl' file for Dataset from images informations
    """
    print("Dataset creation currently processing...")
    start_time = time.time()
    metadata_file = open(save_path + "/metadata.jsonl", "a")

    # BLIP caption generation
    processor = AutoProcessor.from_pretrained(
        "Salesforce/blip-image-captioning-large")
    model = BlipForConditionalGeneration.from_pretrained(
        "Salesforce/blip-image-captioning-large")

    images = [Image.open(save_path + "/" + image_filename)
              for image_filename in images_filename]

    inputs = processor(
        images=images,  return_tensors="pt")

    output = model.generate(
        **inputs, max_new_tokens=50)

    captions = processor.batch_decode(output, skip_special_tokens=True)

    # 'metadata.jsonl' file creation
    for i, caption in enumerate(captions):
        data_input = """{"char_name": "%s", "file_name": "%s", "text": "%s"}\n""" % (
            images_name[i], images_filename[i], caption)

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
