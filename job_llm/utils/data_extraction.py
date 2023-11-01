'''
-----------------------------------------------------------------------
File: data_extraction.py
Creation Time: Oct 31st 2023 2:17 pm
Author: Saurabh Zinjad
Developer Email: zinjadsaurabh1997@gmail.com
Copyright (c) 2023 Saurabh Zinjad. All rights reserved | GitHub: Ztrimus
-----------------------------------------------------------------------
'''

import requests
from bs4 import BeautifulSoup

def get_link_content(url: str):
    """ Extract text content from any given web page

    Args:
        url (str): Webpage web link
    """    
    # getting response object
    res = requests.get(url)
    
    # Initialize the object with the document
    soup = BeautifulSoup(res.content, "html.parser")
    
    # Get the whole body tag
    tag = soup.body
    text_content = ""
    
    # Print each string recursively
    for string in tag.strings:
        string = string.strip()
        if string:
            text_content += string + "\n"

    return text_content