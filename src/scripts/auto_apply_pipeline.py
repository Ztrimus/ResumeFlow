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

print("\n\nStarting Auto Apply Pipeline...")
job_url = "https://careers.eisneramper.com/en/career-opportunities/2301/software-developer-consulting-internship-summer-2024-baton-rouge/?ref=Simplify"
user_data_path = "master_data/saurabh_profile.json"

output_dir = os.path.realpath("output")

print("Fetching User data...")
with open(user_data_path) as json_file:
    user_data = json.load(json_file)

autoApply = AutoApplyModel(openai_key=OPENAI_API_KEY)

print("Extracting Job Details...")
job_details = autoApply.extract_job_details(job_url) # job_details = read_json("logs/Eisneramper_SoftwareDeveloper-ConsultingInternshipSummer2024_JD.json")

doc_name = job_doc_name(job_details)
resume_path = os.path.join(output_dir, f"{doc_name}_resume.json")
cv_path = os.path.join(output_dir, f"{doc_name}_cv.txt")

print("Generating Resume Details...")
resume_details = autoApply.generate_resume_details(job_details, user_data) # resume_details = read_json("output/Eisneramper_SoftwareDeveloper-ConsultingInternshipSummer2024_resume.json")
write_json(resume_path, resume_details)
resume_pdf = latex_to_pdf(resume_details, resume_path.replace(".json", ".pdf"))


print("Generating Cover Letter...")
cv = autoApply.generate_cover_letter(job_details, user_data) # cv = read_file("output/Eisneramper_SoftwareDeveloper-ConsultingInternshipSummer2024_cv.txt")
write_file(cv_path, cv)
is_cv_to_pdf = input("Want cover letter as PDF? (y/n): ")
if is_cv_to_pdf.strip().lower() == "y":
    text_to_pdf(cv, cv_path.replace(".txt", ".pdf"))