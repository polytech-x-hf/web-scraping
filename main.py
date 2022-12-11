# coding=utf-8
# Copyright 2022, Polytech Sorbonne and HuggingFace Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
""" Web scrapping tool to scrap any text / image pair from the web"""

from scrapper.utils import create_dataset
from scrapper.utils import save_dataset
from scrapper.utils import set_const
from Dataset.utils import export_dataset
import os

import argparse

DATASET_PATH = "./assets"
DATASET_IMAGE_EXTENSION = ".jpg"

JOJO_PAGE_LINK = "https://jojo.fandom.com/"
JOJO_CHARS_LIST_LINK = "https://jojo.fandom.com/wiki/Category:Characters"
JOJO_CHARACTER_CLASS = "category-page__member-link"
JOJO_TARGET_CLASS = "image image-thumbnail"
JOJO_CHAR_NAME_FILENAME = "JojosCharactersNames.txt"
JOJO_DATASET_PATH = "./assets/train/jojo"
JOJO_IMAGE_NAME = "JojosImages"

ONEPIECE_PAGE_LINK = ""
ONEPIECE_CHARS_LIST_LINK = ""
ONEPIECE_CHARACTER_CLASS = ""
ONEPIECE_TARGET_CLASS = ""
ONEPIECE_CHAR_NAME_FILENAME = "OnePieceCharactersNames.txt"
ONEPIECE_DATASET_PATH = "./assets/train/onepiece"
ONEPIECE_IMAGE_NAME = "OnepiecesImages"

MAX_IMAGES = -1

SCRIPT_ACTION = ""


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--action", type=str,
                        help="Script action: either 'scrapping' or 'load_dataset", required=True)
    parser.add_argument("--main_page", type=str,
                        help="The web page were the list of characters is", required=False)
    parser.add_argument("--image_names", type=str,
                        help="the names for the image", required=False)
    parser.add_argument("--images_html_class", type=str,
                        help="the html class were all the character's images are", required=False)
    parser.add_argument("--max_images", type=int,
                        help="Max number of images to be scrapped", required=False)
    #parser.add_argument("--chars-list-link", type=str, help="Page link of the character list", required=True)
    #parser.add_argument("--character-class", type=str, help="Class of the characters", required=True)
    #parser.add_argument("--target-class", type=str, help="Image of the character", required=True)
    #parser.add_argument("--char-name-filename", type=str, help="Name of character names file", required=True)
    #parser.add_argument("--dataset-path", type=str, help="Path of the dataset", required=True)
    #parser.add_argument("--image-name", type=str, help="Character image file name", required=True)

    return parser.parse_args()


def set_const_to_utils():
    set_const(DATASET_PATH, DATASET_IMAGE_EXTENSION, JOJO_PAGE_LINK, JOJO_CHARS_LIST_LINK, JOJO_CHARACTER_CLASS, JOJO_TARGET_CLASS,
              JOJO_CHAR_NAME_FILENAME, JOJO_DATASET_PATH, JOJO_IMAGE_NAME, ONEPIECE_PAGE_LINK, ONEPIECE_CHARS_LIST_LINK,
              ONEPIECE_CHARACTER_CLASS, ONEPIECE_TARGET_CLASS, ONEPIECE_CHAR_NAME_FILENAME,
              ONEPIECE_DATASET_PATH, ONEPIECE_IMAGE_NAME, MAX_IMAGES)


def scrapping(args):
    os.system("rm -rf assets/train/jojo")

    if args.main_page != None:
        global JOJO_CHARS_LIST_LINK, JOJO_IMAGE_NAME, JOJO_TARGET_CLASS, MAX_IMAGES
        JOJO_CHARS_LIST_LINK = args.main_page
    if args.image_names != None:
        JOJO_IMAGE_NAME = args.image_names
    else:
        JOJO_IMAGE_NAME = "image"

    if args.images_html_class != None:
        JOJO_TARGET_CLASS = args.images_html_class

    if args.max_images != None:
        MAX_IMAGES = args.max_images

    print("Scrapping in progress...")
    set_const_to_utils()
    save_dataset(True, False)
    dataSet = create_dataset(True, False).to_JSON().replace(
        "[", "").replace("},", "}").replace("]", "").replace("\r\n", "\n")
    file = open("assets/train/jojo/metadata.jsonl", "a")
    file.write(dataSet)
    print("Data scrapped successfuly !")


def main():
    args = get_args()
    if args.action == "scrapping":
        scrapping(args)
    else:
        export_dataset()


if(__name__ == "__main__"):
    main()
