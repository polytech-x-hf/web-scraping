# Work in progress...
import unittest
from Dataset.utils import caption_dataset
from datasets import load_dataset


class DatasetTest(unittest.TestCase):
    """ Test functions in Dataset script """

    def test_load_dataset(self):
        """ Test if dataset is loaded successfuly """
        self.assertIsNotNone(load_dataset("imagefolder", data_dir="assets"))

    def test_caption_dataset(self):
        """ Test if image path exists before captionning """
        self.assertIsNone(caption_dataset("/assets/train/jojo/image0.jpg"))


def main():
    unittest.main()
