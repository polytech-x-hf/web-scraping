from bs4 import BeautifulSoup
import time
import requests
import os
from urllib.parse import urlparse
from urllib.request import urlretrieve
from slugify import slugify

from scraper.export_dataset import create_metadata_from_images


def get_profile_links(url: str):
    """
        Function that get all character profile page link 
    """

    start_time = time.time()

    results = []
    url_domain = urlparse(url).scheme + "://" + urlparse(url).netloc

    req = requests.get(url)

    html_doc = req.text
    soup = BeautifulSoup(html_doc, 'html.parser')

    # category-page__member-link
    html_links = soup.find_all(
        'a', class_="category-page__member-link", recursive=True)

    for link in html_links:
        if(link is not None):
            profile_link = url_domain + link["href"]
            len(profile_link.split("/")) == 6 and results.append(profile_link)

    print("[TIME] get_profile_links(): %.5ss" %
          (time.time() - start_time))

    return results


def get_image_from_link(links: list[str], save_path: str, max_images: int = -1):
    """
        Function that download all images based on links
        Returns image path, image filename and image name
    """

    # Check whether the specified path exists or not
    isExist = os.path.exists(save_path)
    if not isExist:
        # Create a new directory because it does not exist
        os.makedirs(save_path)

    start_time = time.time()
    max_to_download = len(links) if max_images < 0 else max_images

    images_filename = []
    images_name = []

    i = 0

    while(len(images_filename) < max_to_download and i < len(links)-1):
        req = requests.get(links[i])
        html_doc = req.text
        soup = BeautifulSoup(html_doc, 'html.parser')

        character_images = soup.select("img.pi-image-thumbnail")
        character_name = soup.select("h2.pi-title")

        if(len(character_images) > 0):
            # Getting only the 'anime' version if manga is also available
            image = character_images[0]

            data_image_name = [''.join(
                image["data-image-name"].split(".")[:-1]), image["data-image-name"].split(".")[-1]]

            image_url = image["src"]
            image_name = character_name[0].text
            image_filename = slugify(
                data_image_name[0]) + "." + data_image_name[1]

            if(len(image_url.split("/")) == 10 or len(image_url.split("/")) == 12):
                urlretrieve(image_url, save_path + "/" + image_filename)
                images_filename.append(image_filename)
                images_name.append(image_name)

        i += 1

    print("[TIME] get_image_from_link(): %.5ss" %
          (time.time() - start_time))

    return save_path, images_filename, images_name


def jojo_scraping(max_images: int):
    profile_links = get_profile_links(
        "https://jjba.fandom.com/fr/wiki/Cat%C3%A9gorie:Personnages")

    save_path, images_filename, images_name = get_image_from_link(
        profile_links, "assets/train/jojo", max_images)

    return save_path, images_filename, images_name
