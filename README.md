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
Arguments : action (ex : scraping), main_page (ex : https://www.fandom.com), image_names (ex : my_image_name), images_html_class (name of the html class where the link of the image is stocked, example for Jojo's scraping : image image-thumbnail), max_images (number maximal of images wanted, ex : 10)

### Liens

<a href="https://https://www.fandom.com//" target="_blank">Fandom.com</a>

<a href="https://beautiful-soup-4.readthedocs.io/en/latest//" target="_blank">Beatiful Soup documentation</a>

