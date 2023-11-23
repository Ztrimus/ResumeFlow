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
from utils.utils import read_json, write_file, write_json, job_doc_name, save_log

print("Starting Auto Apply Pipeline...")
job_url = "https://careers.eisneramper.com/en/career-opportunities/2301/software-developer-consulting-internship-summer-2024-baton-rouge/?ref=Simplify"
output_dir = "output"

print("Fetching User data...")
with open("master_data/saurabh-profile.json") as json_file:
    user_data = json.load(json_file)

autoApply = AutoApplyModel(openai_key=OPENAI_API_KEY)

print("Extracting Job Details...")
job_details = autoApply.extract_job_details(job_url) # job_details = read_json("logs/job_details.json")
doc_name = job_doc_name(job_details) # save_log(json.dumps(job_details), doc_name)

print("Generating Resume Details...")
resume_details = autoApply.generate_resume_details(job_details, user_data) # resume_details = read_json("logs/Eisneramper_SoftwareDeveloper-ConsultingInternshipSummer2024_resume.json")
resume_path = os.path.join(output_dir, f"{doc_name}_resume.json")
write_json(resume_path, resume_details)

print("Generating Cover Letter...")
cover_letter = autoApply.generate_cover_letter(job_details, user_data)
cover_letter_path = os.path.join(output_dir, f"{doc_name}_cv.txt")
write_file(cover_letter_path, cover_letter)