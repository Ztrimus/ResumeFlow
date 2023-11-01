'''
-----------------------------------------------------------------------
Author: Saurabh Zinjad
Developer Email: zinjadsaurabh1997@gmail.com
File: data_extraction.py
Creation Time: Oct 31st 2023 2:17 pm
Copyright (c) 2023 Saurabh Zinjad. All rights reserved | GitHub: Ztrimus
-----------------------------------------------------------------------
'''

import requests
from bs4 import BeautifulSoup
 
# url of the website 
doc = "https://www.linkedin.com/jobs/view/3749167580"
 
# getting response object
res = requests.get(doc)
 
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

print(text_content)