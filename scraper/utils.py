from bs4 import BeautifulSoup
import requests
from urllib.request import urlretrieve
import os
from Class.DataSet import *
from Dataset.utils import *


def set_const(dataset_path, image_extension, jojo_page, jojo_chars_link, jojo_char_class, jojo_target_class, jojo_char_name_filename,
              jojo_dataset_path, jojo_img_name, onep_page_link, onep_chars_link, onep_char_class, onep_target_class, onep_char_name_filename,
              onep_dataset_path, onep_image_name, max_images):
    global DATASET_PATH, DATASET_IMAGE_EXTENSION, JOJO_PAGE_LINK, JOJO_CHARS_LIST_LINK, JOJO_CHARACTER_CLASS, JOJO_TARGET_CLASS
    global JOJO_CHAR_NAME_FILENAME, JOJO_DATASET_PATH, JOJO_IMAGE_NAME, ONEPIECE_PAGE_LINK, ONEPIECE_CHARS_LIST_LINK
    global ONEPIECE_CHARACTER_CLASS, ONEPIECE_TARGET_CLASS, ONEPIECE_CHAR_NAME_FILENAME, ONEPIECE_DATASET_PATH, ONEPIECE_IMAGE_NAME
    global MAX_IMAGES
    DATASET_PATH, DATASET_IMAGE_EXTENSION, JOJO_PAGE_LINK, JOJO_CHARS_LIST_LINK = dataset_path, image_extension, jojo_page, jojo_chars_link
    JOJO_CHARACTER_CLASS, JOJO_TARGET_CLASS, JOJO_CHAR_NAME_FILENAME = jojo_char_class, jojo_target_class, jojo_char_name_filename
    JOJO_DATASET_PATH, JOJO_IMAGE_NAME, ONEPIECE_PAGE_LINK, ONEPIECE_CHARS_LIST_LINK = jojo_dataset_path, jojo_img_name, onep_page_link, onep_chars_link
    ONEPIECE_CHARACTER_CLASS, ONEPIECE_TARGET_CLASS, ONEPIECE_CHAR_NAME_FILENAME = onep_char_class, onep_target_class, onep_char_name_filename
    ONEPIECE_DATASET_PATH, ONEPIECE_IMAGE_NAME = onep_dataset_path, onep_image_name
    MAX_IMAGES = max_images


def get_image_from_link(link: str, image_class: str, image_name: str, save_path: str):
    """ 
        function to get an image from a link 
    """
    tmp = requests.get(link)
    html_doc = tmp.text
    soup = BeautifulSoup(html_doc, 'html.parser')
    links = soup.find_all('a', class_=image_class, limit=1)
    img_links = []
    for link in links:
        img_links.append(link.get('href'))
    if(len(img_links) >= 1):
        urlretrieve(img_links[0], save_path + "/" + image_name)


def get_characters_links(page_link: str, chars_list_link: str, characters_class: str):
    """ 
        function that return the name and the link of the characters 
    """
    chars_names = []
    chars_links = []

    tmp = None
    try:
        tmp = requests.get(chars_list_link)
    except:
        raise(ValueError("The link : " + chars_list_link +
              " is an incorrent website link"))

    html_doc = tmp.text
    soup = BeautifulSoup(html_doc, 'html.parser')
    links = soup.find_all('a', class_=characters_class)

    if(len(links) <= 0):
        raise(ValueError("No tag with the class : " + characters_class +
              " was found in the link : " + chars_list_link))

    for link in links:
        link_suffixe = link.get('href')
        if ("Category:" in link_suffixe):
            (tmp_names, lst_tmp_links) = get_characters_links(
                page_link, page_link + link_suffixe, characters_class)
            if(len(tmp_names) == len(lst_tmp_links) and len(tmp_names) != 0):
                for i in range(0, len(tmp_names)):
                    chars_links.append(lst_tmp_links[i])
                    chars_names.append(tmp_names[i])
                    if MAX_IMAGES > 0 and len(chars_links) >= MAX_IMAGES:
                        break
            elif(len(tmp_names) != len(lst_tmp_links)):
                raise(ValueError("ERROR : size exceeded"))
        else:
            chars_links.append(page_link + link_suffixe)
            chars_names.append(link.get('title'))
        if MAX_IMAGES > 0 and len(chars_links) >= MAX_IMAGES:
            break

    return (chars_names, chars_links)


def get_one_piece_link():

    return ([], [])
    # encore des bug a fix...
    one_piece_chars_link = "https://onepiece.fandom.com/wiki/List_of_Canon_Characters"
    char_table_class = "wikitable sortable jquery-tablesorter"

    tmp = requests.get(one_piece_chars_link)
    html_doc = tmp.text
    soup = BeautifulSoup(html_doc, 'html.parser')

    chars_names = []
    chars_links = []

    # get the tree tables where the characters link page and names are.
    tables = soup.find_all(
        'table', class_="wikitable sortable", recursive=True)
    for table in tables:
        # foreach table, we get the <tr> html tag that represent a row of the table
        trs = table.find_all('tr')
        # foreach tr tag, we get the 2nd <td> tag where the name and the link of the character is.
        for tr in trs:
            tds = tr.find_all('a', recursive=False)
            chars_names.append(tds[1].get('title'))
            chars_links.append(tds[1].get('href'))

    return (chars_names, chars_links)


def save_all_images_and_names_with_link(main_page_link: str, chars_list_link: str, characters_class: str, image_class: str, images_name: str, image_extension: str, file_text_name: str, path: str, isOnePieceScrapping: bool = False):
    """ 
        function that saves all the images names and links of the characters 
    """
    if(not os.path.exists(path)):
        os.mkdir(path)

    chars_name, char_links = 0, 0
    if isOnePieceScrapping:
        (chars_name, char_links) = get_one_piece_link()
    else:
        (chars_name, char_links) = get_characters_links(
            main_page_link, chars_list_link, characters_class)

    if(len(char_links) != len(chars_name)):
        raise ValueError(
            "ERROR : chars_list_link and charsName doesn't have the same len")

    file = open(path + "/" + file_text_name, "a")

    index = 0
    while len(char_links) > 0:
        name = chars_name.pop(0)
        link = char_links.pop(0)
        if (not name in chars_name) and (not link in char_links):
            get_image_from_link(link, image_class, images_name +
                                str(index) + image_extension, path)
            file.write(name + "\n")
            index += 1

    """
    for i in range(0, len(char_links)):
        get_image_from_link(char_links[i], image_class, images_name + str(i) + image_extension, path)
        file.write(chars_name[i] + "\n")
    """
    file.close()


def save_dataset(jojos_data=True, onepieces_data=True):
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
        save_all_images_and_names_with_link(JOJO_PAGE_LINK, JOJO_CHARS_LIST_LINK, JOJO_CHARACTER_CLASS,
                                            JOJO_TARGET_CLASS, JOJO_IMAGE_NAME, DATASET_IMAGE_EXTENSION, JOJO_CHAR_NAME_FILENAME, JOJO_DATASET_PATH)

    if(onepieces_data):
        save_all_images_and_names_with_link(ONEPIECE_PAGE_LINK, ONEPIECE_CHARS_LIST_LINK, ONEPIECE_CHARACTER_CLASS, ONEPIECE_TARGET_CLASS,
                                            ONEPIECE_IMAGE_NAME, DATASET_IMAGE_EXTENSION, ONEPIECE_CHAR_NAME_FILENAME, ONEPIECE_DATASET_PATH, True)


def create_dataset(jojo_image=True, one_piece_image=True):
    """" 
        Return a Dataset object fill with the data found in the dataset path 
    """

    def fill_dataset(data_path, char_name_path, image_name):
        char_names = []
        file = open(data_path + "/" + char_name_path)

        for line in file:
            char_names.append(line)

        for i in range(0, len(char_names)):
            file_name = image_name + str(i) + DATASET_IMAGE_EXTENSION
            item = DataSetItem(file_name, char_names[i].replace(
                '\n', ''), caption_dataset(data_path + "/" + file_name))
            res.add_item(item)

    res = DataSet()
    if(jojo_image):
        fill_dataset(JOJO_DATASET_PATH,
                     JOJO_CHAR_NAME_FILENAME, JOJO_IMAGE_NAME)

    if(one_piece_image):
        fill_dataset(ONEPIECE_DATASET_PATH,
                     ONEPIECE_CHAR_NAME_FILENAME, ONEPIECE_IMAGE_NAME)

    return res
