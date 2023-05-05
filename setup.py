from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'A package for the model with Jojo and One Piece'

# Setting up
setup(
    name="Jojo&OnePieceModel",
    version = VERSION,
    author = "Polytech-x-hf-MAIN4",
    #author_mail = "",
    url="https://github.com/polytech-x-hf/web-scraping",
    description = DESCRIPTION,
    packages = find_packages(),
    install_requires=find_packages(),
    keywords=['python', 'stable diffusion'],
    
)