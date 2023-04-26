import os
import sys
import time
import slugify
from Scraper.script_onepiece import *
from Scraper.script_jojo import jojo_scraping
from Scraper.export_dataset import create_metadata_from_images, export_dataset


def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
            It must be "yes" (the default), "no" or None (meaning
            an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == "":
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write(
                "Please respond with 'yes' or 'no' " "(or 'y' or 'n').\n")


def removeAssetsFiles(manga_scraped: str):
    """
    Getting authorization before removing files for scrapping
    """

    assetsPath = "assets/train/" + \
        ("onepiece" if (slugify(manga_scraped) in [
         "onepiece", "one-piece"]) else "jojo")

    if (not query_yes_no("Would you like to delete all your assets files in " + assetsPath + " ?")):
        print("Scraping has been aborted...")
        return False

    if(os.path.exists(assetsPath)):
        for file in os.listdir(assetsPath):
            os.remove(assetsPath + "/" + file)

    return True


def scraping(args):

    HUB_PATH = "polytechXhf/jojos-dataset"
    HUB_PATH_TEST = "polytechXhf/jojos-dataset-small"
    HUB_PATH_MIX = "polytechXhf/onepiece-x-jojo-dataset"

    global MAX_IMAGES, MANGA_SCRAPED

    if(args.action in ["scraping", "scrap_and_export"]):
        if(args.manga_scraped == None or not removeAssetsFiles(args.manga_scraped)):
            return

        if args.max_images != None:
            MAX_IMAGES = args.max_images
        else: 
            MAX_IMAGES = -1

        print("Scraping in progress...")

        # Measuring scraping time
        start_time = time.time()

        if(slugify(args.manga_scraped) in ["onepiece", "one-piece"]):
            save_path, images_filename, images_name = onepiece_scraping(
                MAX_IMAGES)
            MANGA_SCRAPED = "onepiece"

        elif(slugify(args.manga_scraped) in ["jojo", "jojos", "jojo-s"]):
            save_path, images_filename, images_name = jojo_scraping(MAX_IMAGES)
            MANGA_SCRAPED = "jojo"

        create_metadata_from_images(save_path, images_filename, images_name)

        print("Scraping finished successfuly in %.4s seconds!" %
              (time.time() - start_time))

    elif (args.action == "export_dataset"):
        if(slugify(args.manga_scraped) in ["onepiece", "one-piece"]):
            MANGA_SCRAPED = "onepiece"
        elif(slugify(args.manga_scraped) in ["jojo", "jojos", "jojo-s"]):
            MANGA_SCRAPED = "jojo"

    if(args.action in ["export_dataset", "scrap_and_export"]):
        export_dataset(MANGA_SCRAPED, HUB_PATH_TEST)
