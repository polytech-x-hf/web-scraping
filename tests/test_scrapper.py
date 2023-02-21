from bs4 import BeautifulSoup
import requests
import unittest
from scraper.utils import *
import pytest
import os

class ScrapperTest(unittest.TestCase):
    """ Test functions in web scrapping script """
    
    def test_get_characters_links():

        errors = []
        (chars_name, char_links) = get_characters_links("https://jojo.fandom.com/", "https://jojo.fandom.com/wiki/Category:Characters",  "category-page__member-link")

        if(len(chars_name) != len(char_links)):
            errors.append("The two result of get_characters_links need to have the same size!")

        if(len(chars_name) > 5):
            errors.append("We set the param MAX_IMAGES to 5 but " + str(len(chars_name)) + " > 5 chars names was returned by the get_characters_links function!")

        if(len(char_links) > 5):
            errors.append("We set the param MAX_IMAGES to 5 but " + str(len(char_links)) + " > 5 chars links was returned by the get_characters_links function!")

        for i in range(0, len(chars_name)):
            if(chars_name[i] in [x for x in chars_name if x != chars_name[i]]):
                errors.append("The caracter name : " + chars_name[i] + " was found multiple time in the result of the get_characters_links function!")

        for i in range(0, len(char_links)):
            if(char_links[i] in [x for x in char_links if x != char_links[i]]):
                errors.append("The caracter link : " + char_links[i] + " was found multiple time in the result of the get_characters_links function!")

        assert len(errors) <= 0, "errors occured:\n".format("\n".join(errors))

    def test_get_image_from_link():

        errors = []
        get_image_from_link("https://jojo.fandom.com/wiki/Arabia_Fats", "image image-thumbnail", "tmp1.jpg", ".")
        get_image_from_link("https://jojo.fandom.com/wiki/Josefumi_Kujo", "image image-thumbnail","tmp2.jpg", ".")
        get_image_from_link("https://jojo.fandom.com/wiki/Bruford", "image image-thumbnail","tmp3.jpg", ".")

        #we try to open the image
        if not os.path.exists("./tmp1.jpg"):
            errors.append("The function get_image_from_link does not save the image from the link : https://jojo.fandom.com/wiki/Arabia_Fats with the image class ; image image-thumbnail")
        else:
            os.remove("./tmp1.jpg")

        if not os.path.exists("./tmp2.jpg"):
            errors.append("The function get_image_from_link does not save the image from the link : https://jojo.fandom.com/wiki/Josefumi_Kujo with the image class ; image image-thumbnail")
        else:
            os.remove("./tmp2.jpg")

        if not os.path.exists("./tmp3.jpg"):
            errors.append("The function get_image_from_link does not save the image from the link : https://jojo.fandom.com/wiki/Bruford with the image class ; image image-thumbnail")
        else:
            os.remove("./tmp3.jpg")

        assert len(errors) <= 0, "errors occured:\n".format("\n".join(errors))

    """def test_web_scraping():
        set_const("./assets", ".jpg", "https://jojo.fandom.com/", "https://jojo.fandom.com/wiki/Category:Characters", "category-page__member-link", "image image-thumbnail", "JojosCharactersNames.txt",
                "./assets/train/jojo", "JojosImages", "", "", "", "", "", "", "", 5)

        test_get_characters_links()
        test_get_image_from_link()
    """

def main():
    unittest.main()