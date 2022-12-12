from datasets import load_dataset

HUB_PATH = "polytechXhf/jojos-dataset"


def export_dataset():
    """
        Create a Dataset from scrapped datas and push it on the hf-hub
    """
    print("Exporting dataset in progress...")

    jojo_dataset = load_dataset("imagefolder", data_dir="assets")

    jojo_dataset.push_to_hub(HUB_PATH)
    print("Dataset exported successfuly !")
