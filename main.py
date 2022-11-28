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

from Class.WebSrapping import create_dataset 
from Class.WebSrapping import save_dataset 

def main():
    #save_dataset(True, False)
    dataSet = create_dataset(True, False)
    file = open("dataSetJSON.json", "a")
    file.write(dataSet.to_JSON())
    pass

if(__name__ == "__main__"):
    main()
