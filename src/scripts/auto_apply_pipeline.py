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

def run_autoapply_pipeline(job_url: str, user_data_path: str = "master_data/saurabh_profile.json"):
    if not len(job_url.strip()):
        print("Job URL is required.")
        return

    print("\n\nStarting Auto Apply Pipeline...")
    autoApply = AutoApplyModel(openai_key=OPENAI_API_KEY)

    print("Fetching User data...")
    if os.path.splitext(user_data_path)[1] == '.pdf':
        user_data = autoApply.get_resume_to_json(user_data_path)
    else:
        user_data = read_json(user_data_path)

    print("Extracting Job Details...")
    # job_details = read_json("output/Eisneramper_SoftwareDeveloper-ConsultingInternshipSummer2024_JD.json")
    job_details = autoApply.extract_job_details(job_url)

    doc_name = job_doc_name(job_details)
    resume_path = os.path.join(output_dir, f"{doc_name}_resume.json")
    cv_path = os.path.join(output_dir, f"{doc_name}_cv.txt")

    print("Generating Resume Details...")
    # resume_details = read_json("output/Eisneramper_SoftwareDeveloper-ConsultingInternshipSummer2024_resume.json")
    resume_details = autoApply.generate_resume_details(job_details, user_data)
    write_json(resume_path, resume_details)
    resume_pdf = latex_to_pdf(resume_details, resume_path.replace(".json", ".pdf"))
    print("Resume PDF generated at: ", resume_path.replace(".json", ".pdf"))


    print("Generating Cover Letter...")
    # cv = read_file("output/Eisneramper_SoftwareDeveloper-ConsultingInternshipSummer2024_cv.txt")
    cv = autoApply.generate_cover_letter(job_details, user_data)
    write_file(cv_path, cv)
    print("Cover Letter generated at: ", cv_path)
    # is_cv_to_pdf = input("Want cover letter as PDF? (y/n): ")
    # if is_cv_to_pdf.strip().lower() == "y":
    text_to_pdf(cv, cv_path.replace(".txt", ".pdf"))
    print("Cover Letter PDF generated at: ", cv_path.replace(".txt", ".pdf"))
    
    print("Done!!!")

if __name__ == "__main__":
    # job_url = "https://careers.eisneramper.com/en/career-opportunities/2301/software-developer-consulting-internship-summer-2024-baton-rouge/?ref=Simplify"
    job_url = "https://www.squarespace.com/careers/jobs/5369485?ref=Simplify"
    run_autoapply_pipeline(job_url)