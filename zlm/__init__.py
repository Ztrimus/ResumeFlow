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

from zlm.utils.llm_models import ChatGPT
from zlm.utils.data_extraction import get_url_content, extract_text
from zlm.utils.utils import get_default_download_folder, measure_execution_time, read_json, write_file, write_json, job_doc_name, text_to_pdf
from zlm.utils.latex_ops import latex_to_pdf


module_dir = os.path.dirname(__file__)
prompt_path = os.path.join(module_dir, 'prompts')


class AutoApplyModel:
    def __init__(self, openai_key: str, downloads_dir: str):
        if openai_key == None or openai_key.strip() == 'os':
            self.openai_key = os.environ.get("OPENAI_API_KEY")

        if downloads_dir == None or downloads_dir.strip() == "":
            self.downloads_dir = get_default_download_folder()
    
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
        if user_data_path == None or user_data_path.strip() == "":
            user_data_path = os.path.join(module_dir, 'demo_data','user_profile.json')

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
        try:
            system_prompt = self.get_system_prompt(os.path.join(prompt_path, "persona-job-llm.txt")) + \
                            self.get_system_prompt(os.path.join(prompt_path, "extract-job-detail.txt"))
            job_site_content = get_url_content(url)

            chat_gpt = ChatGPT(openai_api_key=self.openai_key, system_prompt=system_prompt)
            response = chat_gpt.get_response(job_site_content)
            job_details = json.loads(response)
            jd_path = job_doc_name(job_details, self.downloads_dir, 'jd')
            write_json(jd_path, job_details)
            
            return job_details
        except Exception as e:
            print(e)
            return None
    
    @measure_execution_time
    def resume_builder(self, job_details: dict, user_data: dict):
        system_prompt = self.get_system_prompt(os.path.join(prompt_path, "persona-job-llm.txt")) + \
                        self.get_system_prompt(os.path.join(prompt_path, "generate-resume-details.txt"))
        query = f"""Provided Job description delimited by triple backticks(```) and my resume or work information below delimited by triple dashes(---). ```{json.dumps(job_details)}``` ---{json.dumps(user_data)}---"""
        
        chat_gpt = ChatGPT(openai_api_key=self.openai_key, system_prompt=system_prompt)
        response = chat_gpt.get_response(query, expecting_longer_output=True)
        resume_details = json.loads(response)
        resume_path = job_doc_name(job_details, self.downloads_dir, 'resume')

        write_json(resume_path, resume_details)

        latex_to_pdf(resume_details, resume_path.replace(".json", ".pdf"))
        print("Resume PDF generated at: ", resume_path.replace(".json", ".pdf"))
        return resume_details
    
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
        cv_path = job_doc_name(job_details, self.downloads_dir, 'cv')
        write_file(cv_path, cover_letter)
        print("Cover Letter generated at: ", cv_path)
        is_cv_to_pdf = input("Want cover letter as PDF? (y/n): ")
        if is_cv_to_pdf.strip().lower() == "y":
            text_to_pdf(cover_letter, cv_path.replace(".txt", ".pdf"))
            print("Cover Letter PDF generated at: ", cv_path.replace(".txt", ".pdf"))        
        return cover_letter
    
    def resume_cv_pipeline(self, job_url: str, user_data_path: str):
        """Run the Auto Apply Pipeline.

        Args:
            job_url (str): The URL of the job to apply for.
            user_data_path (str, optional): The path to the user profile data file.
                Defaults to os.path.join(module_dir, "master_data','user_profile.json").

        Returns:
            None: The function prints the progress and results to the console.
        """
        try:
            print("Starting Auto Resume and CV Pipeline")
            if not len(job_url.strip()):
                print("Job URL is required.")
                return

            print("\nFetching User data...")
            user_data = self.user_data_extraction(user_data_path)

            print("\nExtracting Job Details...")
            job_details = self.job_details_extraction(job_url)
            
            print("\nGenerating Resume Details...")
            self.resume_builder(job_details, user_data)

            print("\nGenerating Cover Letter...")
            self.cover_letter_generator(job_details, user_data)
            
            print("Done!!!")
        except Exception as e:
            print(e)
            return None