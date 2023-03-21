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
""" Web scraping tool to scrap any text / image pair from the web"""

import argparse
from tests.test_dataset import *
from tests.test_scrapper import *

from Scraper.main import scraping

MAX_IMAGES = -1


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--action", type=str,
                        help="Script action: either 'scraping', 'export_dataset', 'scrap_and_export' or 'training'", required=True)
    parser.add_argument("--manga_scraped", type=str,
                        help="Scrap either 'jojo' or 'onepiece'", required=True)
    parser.add_argument("--get_tests", type=int,
                        help="Test the scraper (0 or 1)", required=True)
    parser.add_argument("--max_images", type=int,
                        help="Max number of images to be scraped", required=False)

    return parser.parse_args()


def main():
    args = get_args()
    if args.action in ["scraping", "export_dataset", "scrap_and_export"]:
        scraping(args)
        if args.get_tests == 1:
            print("tests...")
    else:
        print("Training is coming...")


if(__name__ == "__main__"):
    main()
