# Web sraping script

The purpose of this script is to retrieve the images and names of the One Piece and JoJo's Bizarre Adventure characters from the Fandom.com website.

Installation required :

```
pip install beautifulsoup4
pip install requests
```

To run locally do the following:

```
git clone https://github.com/polytech-x-hf/web-scraping
python main.py [arguments]
```

Arguments : action (ex : scraping), get_tests (test the scraper, ex : 0 or 1), main_page (ex : https://jojo.fandom.com/), image_names (ex : my_image_name), images_html_class (name of the html class where the link of the image is stocked, example for Jojo's scraping : image image-thumbnail), max_images (number maximal of images wanted, ex : 10 or -1 for all possible images)

For instance :

```
python main.py --action "scraping" --get_tests 1 --main_page "https://jojo.fandom.com/" --image_names "my_image_name" --images_html_class "image image-thumbnail" --max_images 5
```

### Links

<a href="https://https://www.fandom.com//" target="_blank">Fandom.com</a>

<a href="https://beautiful-soup-4.readthedocs.io/en/latest//" target="_blank">Beatiful Soup documentation</a>

# Dataset script

The purpose of this script is to fill the dataset, created by the scraper, with a caption and export it to the hub.

Installation required :

```
pip install datasets
pip install PIL
pip install transformers
```

To run locally do the following:

```
git clone https://github.com/polytech-x-hf/web-scraping
python main.py --action "load_dataset"
```

### Links

<a href="https://huggingface.co/docs/datasets/index" target="_blank">Datasets documentation</a>

<a href="https://he-arc.github.io/livre-python/pillow/index.html" target="_blank">PIL documentation</a>

<a href="https://huggingface.co/docs/transformers/model_doc/blip" target="_blank">Blip documentation</a>

<a href="https://huggingface.co/docs/transformers/model_doc/auto" target="_blank">Autoclasses documentation</a>

<a href="https://huggingface.co/docs/transformers/index" target="_blank">Transformers documentation</a>
