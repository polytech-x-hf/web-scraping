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
from models.finetuned import *
from models.sd import *

MAX_IMAGES = -1


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--action", type=str,
                        help="Script action: either 'scraping', 'export_dataset', 'scrap_and_export' or 'test_model'", required=True)
    parser.add_argument("--manga_scraped", type=str,
                        help="Scrap either 'jojo' or 'onepiece'", required=False)
    parser.add_argument("--get_tests", type=int,
                        help="Test the scraper (0 or 1)", required=False)
    parser.add_argument("--max_images", type=int,
                        help="Max number of images to be scraped", required=False)
    parser.add_argument("--test_prompt", type=str,
                        help="The prompt used for the model test", required=False)
    parser.add_argument("--torch_device", type=str,
                        help="When testing model, 'pipe.to()' device: cuda, mps (MacOS M1), etc...", required=False)

    return parser.parse_args()


def main():
    args = get_args()
    if args.action in ["scraping", "export_dataset", "scrap_and_export"]:
        scraping(args)
        if args.get_tests == 1:
            print("tests...")
    elif args.action == "test_model":
        prompt = args.test_prompt if args.test_prompt else "a photo of an astronaut riding a horse on mars"
        torchDevice = args.torch_device if args.torch_device else "cuda"
        print("Prompt:", prompt)
        print("PyTorch device:", torchDevice)
        model_finetuned(prompt, torchDevice)
        model_SD(prompt, torchDevice)
        print("Images exported to 'model_base.png' and 'model_finetuned.png'")


if(__name__ == "__main__"):
    main()
