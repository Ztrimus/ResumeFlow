'''
Filename: /home/saurabh/AAA/Convergent/Projects/job-llm/zlm/__init__.py
Path: /home/saurabh/AAA/Convergent/Projects/job-llm/zlm
Created Date: Wednesday, December 6th 2023, 7:09:13 pm
Author: Saurabh Zinjad

Copyright (c) 2023 Your Company
'''

from zlm.scripts.auto_apply_pipeline import run_autoapply_pipeline

def create_resume(url, master_data):
    run_autoapply_pipeline(url, master_data)