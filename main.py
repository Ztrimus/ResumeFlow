'''
-----------------------------------------------------------------------
File: main.py
Creation Time: Nov 24th 2023 7:04 pm
Author: Saurabh Zinjad
Developer Email: zinjadsaurabh1997@gmail.com
Copyright (c) 2023 Saurabh Zinjad. All rights reserved | GitHub: Ztrimus
-----------------------------------------------------------------------
'''

import os
import argparse
from zlm import AutoApplyModel

def create_resume_cv(url, master_data, openai_key, downloads_dir):
    job_llm = AutoApplyModel(openai_key, downloads_dir)
    job_llm.resume_cv_pipeline(url, master_data)

if __name__ == "__main__":
    # Create an argument parser
    parser = argparse.ArgumentParser()

    # Add the required arguments

    parser.add_argument('-u', "--url", help='URL of the job posting')
    parser.add_argument('-m', "--master_data", help='Path of user\'s master data file.')
    parser.add_argument('-k', "--openai_api_key", default="os", help='Open AI API Keys')
    parser.add_argument('-d', "--downloads_dir", help='Give detailed path of folder')

    # Parse the arguments
    args = parser.parse_args()
    
    create_resume_cv(args.url, args.master_data, args.openai_api_key, args.downloads_dir)