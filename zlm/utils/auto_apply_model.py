'''
-----------------------------------------------------------------------
File: auto_apply_model.py
Creation Time: Nov 21st 2023 2:49 am
Author: Saurabh Zinjad
Developer Email: zinjadsaurabh1997@gmail.com
Copyright (c) 2023 Saurabh Zinjad. All rights reserved | GitHub: Ztrimus
-----------------------------------------------------------------------
'''
import os
import sys
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.llm_models import ChatGPT
from utils.data_extraction import get_url_content, extract_text
from utils.utils import measure_execution_time, read_json

module_dir = os.path.dirname(__file__)
prompt_path = os.path.join(module_dir, '..', 'prompts')


class AutoApplyModel:
    def __init__(self, openai_key: str):
        self.openai_key = openai_key
    
    def get_system_prompt(self, system_prompt_path: str):
        return open(system_prompt_path).read().strip()+"\n"

    def get_resume_to_json(self, pdf_path):
        system_prompt = self.get_system_prompt(os.path.join(prompt_path, "resume-extractor.txt"))
        chat_gpt = ChatGPT(openai_api_key=self.openai_key, system_prompt=system_prompt)
        resume_text = extract_text(pdf_path)
        resume_text = chat_gpt.get_response(resume_text)
        resume_json = json.loads(resume_text)
        return resume_json
    
    @measure_execution_time
    def user_data_extraction(self, user_data_path: str):
        if os.path.splitext(user_data_path)[1] == '.pdf':
            return self.get_resume_to_json(user_data_path)
        else:
            return read_json(user_data_path)

    @measure_execution_time
    def job_details_extraction(self, url: str):
        """
        Extracts job details from the specified job URL.

        Args:
            url (str): The URL of the job posting.

        Returns:
            dict: A dictionary containing the extracted job details.
        """
        system_prompt = self.get_system_prompt(os.path.join(prompt_path, "persona-job-llm.txt")) + \
                        self.get_system_prompt(os.path.join(prompt_path, "extract-job-detail.txt"))
        job_site_content = get_url_content(url)

        chat_gpt = ChatGPT(openai_api_key=self.openai_key, system_prompt=system_prompt)
        response = chat_gpt.get_response(job_site_content)
        job_details = json.loads(response)
        
        return job_details
    
    @measure_execution_time
    def resume_builder(self, job_details: dict, user_data: dict):
        system_prompt = self.get_system_prompt(os.path.join(prompt_path, "persona-job-llm.txt")) + \
                        self.get_system_prompt(os.path.join(prompt_path, "generate-resume-details.txt"))
        query = f"""Provided Job description delimited by triple backticks(```) and my resume or work information below delimited by triple dashes(---). ```{json.dumps(job_details)}``` ---{json.dumps(user_data)}---"""
        
        chat_gpt = ChatGPT(openai_api_key=self.openai_key, system_prompt=system_prompt)
        response = chat_gpt.get_response(query, expecting_longer_output=True)
        job_details = json.loads(response)
        return job_details
    
    @measure_execution_time
    def cover_letter_generator(self, job_details: dict, user_data: dict):
        system_prompt = self.get_system_prompt(os.path.join(prompt_path, "persona-job-llm.txt")) + \
                        self.get_system_prompt(os.path.join(prompt_path, "generate-cover-letter.txt"))
        query = f"""Provided Job description delimited by triple backticks(```) and \
                    my resume or work information below delimited by triple dashes(---).
                    ```
                    {json.dumps(job_details)}
                    ```

                    ---
                    {json.dumps(user_data)}
                    ---
                """
        
        chat_gpt = ChatGPT(openai_api_key=self.openai_key, system_prompt=system_prompt)
        cover_letter = chat_gpt.get_response(query, expecting_longer_output=True)
        return cover_letter