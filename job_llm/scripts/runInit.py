'''
-----------------------------------------------------------------------
File: LLM.py
Creation Time: Nov 1st 2023 1:40 am
Author: Amey Bhilegaonkar
Developer Email: abhilega@asu.edu
Copyright (c) 2023 Amey Bhilegaonkar. All rights reserved | GitHub: ameygoes
-----------------------------------------------------------------------
'''

import openai
import sys
import openai
sys.path.append('../')

from job_llm.utils.data_extraction import get_url_content, extract_text
from job_llm.utils.utils import read_file, write_json, ext

from job_llm import config
from job_llm.utils.llm_models import ChatGPT

resume_prompt = open("./prompts/resume-extractor.txt").read().strip()
# TODO: Consider 2 separate prompts for persona-job-llm and job-details-extractor
job_prompt = open("./prompts/job-detail-extractor.txt").read().strip()
compare_prompt = open("./prompts/compare-prompt.txt").read().strip()

def createGPTs():
    resumeGPT = ChatGPT(openai_api_key=config.OPENAI_API_KEY, system_prompt=resume_prompt)
    jobGPT = ChatGPT(openai_api_key=config.OPENAI_API_KEY, system_prompt=job_prompt)
    compareGPT = ChatGPT(openai_api_key=config.OPENAI_API_KEY, system_prompt=compare_prompt)
    return [resumeGPT, jobGPT, compareGPT]


resumeGPT, jobGPT, compareGPT = createGPTs()

# parse resume
pdf_path = '../input/Amey_Bhilegaonkar_Resume.pdf'
resume_text = extract_text(pdf_path)
output_json_path = '../output/ameyBhilegaonkar.json'

# parse resume and save JSON file
pdf_parser.resume_text = resumeGPT.get_response(resume_text)
pdf_parser.save_to_json()

jobDetails = jobGPT.get_response(get_url_content("https://www.linkedin.com/jobs/view/3760365533"))
write_json("../output/job_details.json", jobDetails)

# compare resume and job details and craft resume
resumeContents = read_file("../output/ameyBhilegaonkar.json")
jobContents = read_file("../output/job_details.json")
compareContents = read_file("./prompts/compare-create-resume-from-jd.txt")
compareContents = compareContents.replace("<< RESUME >>", resumeContents).replace("<< DESCRIPTION >>", jobContents)

print(compareContents)
finalResumePrompt = compareGPT.get_response(compareContents)
write_json("../output/final-resume.json", finalResumePrompt)