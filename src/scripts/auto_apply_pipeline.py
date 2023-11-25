'''
-----------------------------------------------------------------------
File: auto-apply-pipeline.py
Creation Time: Nov 21st 2023 4:06 am
Author: Saurabh Zinjad
Developer Email: zinjadsaurabh1997@gmail.com
Copyright (c) 2023 Saurabh Zinjad. All rights reserved | GitHub: Ztrimus
-----------------------------------------------------------------------
'''
import os
import sys
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.auto_apply_model import AutoApplyModel
from config import OPENAI_API_KEY
from utils.utils import read_json, read_file, write_file, write_json, job_doc_name, save_log, text_to_pdf
from utils.latex_ops import latex_to_pdf

output_dir = os.path.realpath("output")

def run_autoapply_pipeline(job_url: str, user_data_path: str = "master_data/user_profile.json"):
    try:
        if not len(job_url.strip()):
            print("Job URL is required.")
            return

        print("\n\nStarting Auto Apply Pipeline...")
        autoApply = AutoApplyModel(openai_key=OPENAI_API_KEY)

        print("\nFetching User data...")
        user_data = autoApply.user_data_extraction(user_data_path)

        print("\nExtracting Job Details...")
        job_details = autoApply.job_details_extraction(job_url)
        jd_path, resume_path, cv_path  = job_doc_name(job_details, output_dir)
        write_json(jd_path, job_details)

        print("\nGenerating Resume Details...")
        resume_details = autoApply.resume_builder(job_details, user_data)
        write_json(resume_path, resume_details)
        latex_to_pdf(resume_details, resume_path.replace(".json", ".pdf"))
        print("Resume PDF generated at: ", resume_path.replace(".json", ".pdf"))


        print("\nGenerating Cover Letter...")
        cv = autoApply.cover_letter_generator(job_details, user_data)
        write_file(cv_path, cv)
        print("Cover Letter generated at: ", cv_path)
        is_cv_to_pdf = input("Want cover letter as PDF? (y/n): ")
        if is_cv_to_pdf.strip().lower() == "y":
            text_to_pdf(cv, cv_path.replace(".txt", ".pdf"))
            print("Cover Letter PDF generated at: ", cv_path.replace(".txt", ".pdf"))
        
        print("Done!!!")
    except Exception as e:
        print(e)
        return None