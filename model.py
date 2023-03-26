from datasets import load_dataset
from PIL import Image
import io

# def convert_image(sample):
#   sample["image"] = Image.open(io.BytesIO(sample["image"]["bytes"]))
#   print("test")
#   return sample

URL_pokemon = "lambdalabs/pokemon-blip-captions"
URL_jojo = "polytechXhf/jojos-dataset-small"
ds = load_dataset(URL_jojo, split="train")
sample = ds[0]
# display(sample["image"].resize((256, 256)))
print(sample["image"])
