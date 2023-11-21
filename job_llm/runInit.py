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

from job_llm.utils.data_extraction import get_link_content, read_file_from_location, write_file_to_location

from job_llm.utils.resume_reader import PDFResumeParser
from job_llm import config
from job_llm.utils.llm_models import ChatGPT

resume_prompt = open("./prompts/resume-extractor.txt").read().strip()
job_prompt = open("./prompts/job-detail-extractor.txt").read().strip()
compare_prompt = open("./prompts/compare-prompt.txt").read().strip()

def createGPTs():
    resumeGPT = ChatGPT(openai_api_key=config.OPENAI_API_KEY, system_prompt=resume_prompt)
    jobGPT = ChatGPT(openai_api_key=config.OPENAI_API_KEY, system_prompt=job_prompt)
    compareGPT = ChatGPT(openai_api_key=config.OPENAI_API_KEY, system_prompt=compare_prompt)
    return [resumeGPT, jobGPT, compareGPT]


resumeGPT, jobGPT, compareGPT = createGPTs()

# parse resume
pdf_parser = PDFResumeParser()
pdf_parser.extract_text()

# parse resume and save JSON file
pdf_parser.resume_text = resumeGPT.get_response(pdf_parser.resume_text)
pdf_parser.save_to_json()

jobDetails = jobGPT.get_response(get_link_content("https://www.linkedin.com/jobs/view/3760365533"))
write_file_to_location("../output/job_details.json", jobDetails)

# compare resume and job details and craft resume
resumeContents = read_file_from_location("../output/ameyBhilegaonkar.json")
jobContents = read_file_from_location("../output/job_details.json")
compareContents = read_file_from_location("./prompts/compare-create-resume-from-jd.txt")
compareContents = compareContents.replace("<< RESUME >>", resumeContents).replace("<< DESCRIPTION >>", jobContents)

print(compareContents)
finalResumePrompt = compareGPT.get_response(compareContents)
write_file_to_location("../output/final-resume.json", finalResumePrompt)