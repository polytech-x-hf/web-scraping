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

import argparse


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset_path", type=str,
                        help="Path to the final dataset", required=False)
    #parser.add_argument("--dataset-image-extension", type=str, help="Extension of image files", required=True)
    #parser.add_argument("--page-link", type=str, help="Page link", required=True)
    #parser.add_argument("--chars-list-link", type=str, help="Page link of the character list", required=True)
    #parser.add_argument("--character-class", type=str, help="Class of the characters", required=True)
    #parser.add_argument("--target-class", type=str, help="Image of the character", required=True)
    #parser.add_argument("--char-name-filename", type=str, help="Name of character names file", required=True)
    #parser.add_argument("--dataset-path", type=str, help="Path of the dataset", required=True)
    #parser.add_argument("--image-name", type=str, help="Character image file name", required=True)

    return parser.parse_args()


def main():
    args = get_args()
    dataset_path = args.dataset_path

    save_dataset(True, False)
    # dataSet = create_dataset(True, False)
    # file = open("dataSetJSON.json", "a")
    # file.write(dataSet.to_JSON())
    pass


if(__name__ == "__main__"):
    main()
