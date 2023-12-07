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
    parser.add_argument('-m', "--master_data", default="master_data/user_profile.json", help='Path of user\'s master data file.')
    parser.add_argument('-k', "--openai_api_key", default="os", help='Open AI API Keys')
    parser.add_argument('-d', "--downloads_dir", help='Give detailed path of folder')

    # Parse the arguments
    args = parser.parse_args()

    args.url = "https://boards.greenhouse.io/thebrattlegroup/jobs/4325755005"
    args.master_data = "/home/saurabh/AAA/Convergent/Projects/job-llm/master_data/user_profile.json"

    if args.openai_api_key == 'os':
        args.openai_api_key = os.environ.get("OPENAI_API_KEY")
    
    create_resume_cv(args.url, args.master_data, args.openai_api_key, args.downloads_dir)