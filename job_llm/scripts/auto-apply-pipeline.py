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
from utils.utils import write_file, job_doc_name, save_log

job_url = "https://careers.eisneramper.com/en/career-opportunities/2301/software-developer-consulting-internship-summer-2024-baton-rouge/?ref=Simplify"
output_dir = "output"
with open("master_data/saurabh-profile.json") as json_file:
    user_data = json.load(json_file)

autoApply = AutoApplyModel(openai_key=OPENAI_API_KEY)

# job_details = autoApply.extract_job_details(job_url)
with open("output/job_details.json") as json_file:
    job_details = json.load(json_file)
doc_name = job_doc_name(job_details)
save_log(json.dumps(job_details), doc_name)

resume_details = autoApply.generate_resume_details(job_details, user_data)
save_log(json.dumps(resume_details), doc_name)
resume_path = os.path.join(output_dir, f"{doc_name}_resume.json")
#TODO: Amey - JSON to Resume PDF formatting function
write_file(resume_path, resume_details)

cover_letter = autoApply.generate_cover_letter(job_details, user_data)
save_log(cover_letter, doc_name)
cover_letter_path = os.path.join(output_dir, f"{doc_name}_cv.txt")
write_file(cover_letter_path, cover_letter)