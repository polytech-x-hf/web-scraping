from datasets import load_dataset

jojo_dataset = load_dataset(
    "json", data_files="https://huggingface.co/datasets/polytechXhf/jojos-dataset/raw/main/jojo.json", field="items")
print("Jojo:", jojo_dataset["train"][2])