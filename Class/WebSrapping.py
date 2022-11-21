from bs4 import BeautifulSoup
import requests
from urllib.request import urlretrieve
import os
from const import *
from Class.DataSet import *

def get_image_from_link(link:str, image_class:str, image_name:str, save_path:str):
    """ 
        function to get an image from a link 
        
    """
    tmp = requests.get(link)
    html_doc = tmp.text
    soup = BeautifulSoup(html_doc, 'html.parser')
    links = soup.find_all('a', class_ = image_class, limit=1)#a = soup.find_all('a', id = targetedID)
    img_links = []
    for link in links:
        img_links.append(link.get('href'))
    if(len(img_links) >= 1):
        urlretrieve(img_links[0], save_path + "/" + image_name)

def get_characters_links(page_link:str, chars_list_link:str, characters_class:str):
    """ 
        function that return the name and the link of the characters 
        
    """
    chars_names = []
    chars_links = []
    tmp = requests.get(chars_list_link)
    html_doc = tmp.text
    soup = BeautifulSoup(html_doc, 'html.parser')
    links = soup.find_all('a', class_ = characters_class)
    for link in links:
        link_suffixe = link.get('href')
        if ("Category:" in link_suffixe):
            (tmp_names, lst_tmp_links) = get_characters_links(page_link, chars_list_link + link_suffixe, characters_class)
            if(len(tmp_names) == len(lst_tmp_links) and len(tmp_names) != 0):
                for i in range(0, len(tmp_names)):
                    chars_links.append(lst_tmp_links[i])
                    chars_names.append(tmp_names[i])
            elif(len(tmp_names) == len(lst_tmp_links)):
                raise(
                    ValueError("ERROR : size exceeded")
                )
        else:
            chars_links.append(page_link + link_suffixe)
            chars_names.append(link.get('title'))

    return (chars_names, chars_links)

def save_all_images_and_names_with_link(main_page_link:str, chars_list_link:str, characters_class:str, image_class:str, images_name:str, image_extension:str, file_text_name:str, path:str):
    """ 
        function that saves all the imagess names and links of the characters 
        
    """
    if(not os.path.exists(path)):
        os.mkdir(path)
    (chars_name, char_links) = get_characters_links(main_page_link, chars_list_link, characters_class)
    if(len(char_links) != len(chars_name)):
        raise ValueError(
            "ERROR : charsListLink and charsName doesn't have the same len"
            )
    file = open(path + "/" + file_text_name, "a")
    for i in range(0, len(char_links)):
        get_image_from_link(char_links[i], image_class, images_name + str(i) + image_extension, path)
        file.write(chars_name[i] + "\n")
    file.close()

def save_dataset(jojos_data = True, onepieces_data = True):
    """"
        Download files and set data content in the data directory
        
    """
    if(not os.path.exists(DATASET_PATH)):
        os.mkdir(DATASET_PATH)
    if(not os.path.exists(JOJO_DATASET_PATH)):
        os.mkdir(JOJO_DATASET_PATH)
    if(not os.path.exists(ONEPIECE_DATASET_PATH)):
        os.mkdir(ONEPIECE_DATASET_PATH)
    
    if(jojos_data):
        save_all_images_and_names_with_link(JOJO_PAGE_LINK, JOJO_CHARS_LIST_LINK, JOJO_CHARACTER_CLASS, JOJO_TARGET_CLASS, JOJO_IMAGE_NAME, DATASET_IMAGE_EXTENSION, JOJO_CHAR_NAME_FILENAME, JOJO_DATASET_PATH)

    if(onepieces_data):
        save_all_images_and_names_with_link(ONEPIECE_PAGE_LINK, ONEPIECE_CHARS_LIST_LINK, ONEPIECE_CHARACTER_CLASS, ONEPIECE_TARGET_CLASS, ONEPIECE_IMAGE_NAME, DATASET_IMAGE_EXTENSION, ONEPIECE_CHAR_NAME_FILENAME, ONEPIECE_DATASET_PATH)

def create_dataset(jojo_image = True, one_piece_image = True):
    """" 
        Return a Dataset object fill with the data found in the dataset path 
    """

    def fil_dataset(data_path, char_name_path, image_name):
        char_names = []
        file = open(data_path + "/" + char_name_path)
        for line in file:
            char_names.append(line)
        for i in range(0, len(char_names)):
            item = DataSetItem(image_name + str(i) + DATASET_IMAGE_EXTENSION, char_names[i].replace('\n', ''))
            res.add_item(item)
        
    res = DataSet()
    if(jojo_image):
        fil_dataset(JOJO_DATASET_PATH, JOJO_CHAR_NAME_FILENAME, JOJO_IMAGE_NAME)

    if(one_piece_image):
        fil_dataset(ONEPIECE_DATASET_PATH, ONEPIECE_CHAR_NAME_FILENAME, ONEPIECE_IMAGE_NAME)

    return res