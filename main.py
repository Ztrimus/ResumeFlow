'''
-----------------------------------------------------------------------
File: main.py
Creation Time: Nov 24th 2023 7:04 pm
Author: Saurabh Zinjad
Developer Email: zinjadsaurabh1997@gmail.com
Copyright (c) 2023 Saurabh Zinjad. All rights reserved | GitHub: Ztrimus
-----------------------------------------------------------------------
'''

import argparse
from zlm.scripts.auto_apply_pipeline import run_autoapply_pipeline

def create_resume(url, master_data):
    run_autoapply_pipeline(url, master_data)

if __name__ == "__main__":
    # Create an argument parser
    parser = argparse.ArgumentParser()

    # Add the required arguments

    parser.add_argument('-u', "--url", help='URL of the job posting')
    parser.add_argument('-m', "--master_data", default="master_data/user_profile.json", help='Path of user\'s master data file.')

    # Parse the arguments
    args = parser.parse_args()

    run_autoapply_pipeline(args.url, args.master_data)