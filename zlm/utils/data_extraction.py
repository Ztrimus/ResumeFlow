'''
-----------------------------------------------------------------------
File: data_extraction.py
Creation Time: Oct 31st 2023 2:17 pm
Author: Saurabh Zinjad, Amey Bhilegonkar
Developer Email: zinjadsaurabh1997@gmail.com, abhilega@asu.edu
Copyright (c) 2023 Saurabh Zinjad. All rights reserved | GitHub: Ztrimus, ameygoes
-----------------------------------------------------------------------
'''
import re
import json
import PyPDF2
import requests
from bs4 import BeautifulSoup
import streamlit as st
from langchain_community.document_loaders import PlaywrightURLLoader, UnstructuredURLLoader, WebBaseLoader

def read_data_from_url(url):
        try: 
            url_content = ""

            basic_selectors = ["header", "footer"]
            linkedin_selectors = ["#main-content > section.right-rail",
                                  ".job-alert-redirect-section", ".similar-jobs"]
            
            # TODO: Filter out selectors bassed on the website
            all_selectors = basic_selectors

            unstr_loader = UnstructuredURLLoader(urls=[url], ssl_verify=False, remove_selectors=all_selectors)
            playwright_loader = PlaywrightURLLoader(urls=[url], remove_selectors=all_selectors)
            web_loader = WebBaseLoader(url)

            pages = []
            for loader in [playwright_loader, unstr_loader, web_loader]:
                pages = loader.load()
                if pages != []:
                    break

            for page in pages:
                if page.page_content.strip() != "":
                    # text = page.extract_text().split("\n")
                    text_list = page.page_content.split("\n")

                    # Remove Unicode characters from each line
                    cleaned_texts = [re.sub(r'[^\x00-\x7F]+', '', line) for line in text_list]
                    cleaned_texts = [text.strip() for text in cleaned_texts if text.strip() not in ['', None]]

                    # Join the lines into a single string
                    cleaned_texts_string = '\n'.join(cleaned_texts)
                    url_content += cleaned_texts_string
                
                return url_content
        except Exception as e:
            print(e)
            return None

def extract_text(pdf_path: str):
    resume_text = ""

    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        num_pages = len(pdf_reader.pages)

        for page_num in range(num_pages):
            page = pdf_reader.pages[page_num]
            text = page.extract_text().split("\n")

            # Remove Unicode characters from each line
            cleaned_text = [re.sub(r'[^\x00-\x7F]+', '', line) for line in text]

            # Join the lines into a single string
            cleaned_text_string = '\n'.join(cleaned_text)
            resume_text += cleaned_text_string
        
        return resume_text

def get_url_content(url: str):
    """ Extract text content from any given web page

    Args:
        url (str): Webpage web link
    """    
    try:
        # getting response object
        res = requests.get(url)
        # Initialize the object with the document
        soup = BeautifulSoup(res.content, "html.parser")
        
        # Get the whole body tag
        tag = soup.body
        text_content = ""
        # TODO: Preprocessing of data, like remove html tags, remove unwanted content, etc.
        
        # Print each string recursively
        for string in tag.strings:
            string = string.strip()
            if string:
                text_content += string + "\n"

        return text_content
    except Exception as e:
        print(e)
        return None