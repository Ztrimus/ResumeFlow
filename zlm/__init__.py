'''
-----------------------------------------------------------------------
File: __init__.py
Creation Time: Feb 8th 2024, 2:59 pm
Author: Saurabh Zinjad
Developer Email: saurabhzinjad@gmail.com
Copyright (c) 2023-2024 Saurabh Zinjad. All rights reserved | https://github.com/Ztrimus
-----------------------------------------------------------------------
'''
import os
import json
import re
import aiohttp
import asyncio
import validators
import numpy as np
import streamlit as st
from typing import Dict, Any


from zlm.utils import utils
from zlm.utils.latex_ops import latex_to_pdf
from zlm.utils.llm_models import ChatGPT, Gemini, TogetherAI
from zlm.utils.data_extraction import get_url_content, extract_text
from zlm.utils.metrics import jaccard_similarity, overlap_coefficient, cosine_similarity, vector_embedding_similarity

from langchain_community.document_loaders import UnstructuredURLLoader
from langchain_community.document_loaders import PlaywrightURLLoader


module_dir = os.path.dirname(__file__)
demo_data_path = os.path.join(module_dir, "demo_data", "user_profile.json")
prompt_path = os.path.join(module_dir, "prompts")


class AutoApplyModel:
    """
    A class that represents an Auto Apply Model for job applications.

    Args:
        api_key (str): The OpenAI API key.
        downloads_dir (str, optional): The directory to save downloaded files. Defaults to the default download folder.

    Attributes:
        api_key (str): The OpenAI API key.
        downloads_dir (str): The directory to save downloaded files.

    Methods:
        get_prompt(system_prompt_path: str) -> str: Returns the system prompt from the specified path.
        resume_to_json(pdf_path: str) -> dict: Extracts resume details from the specified PDF path.
        user_data_extraction(user_data_path: str) -> dict: Extracts user data from the specified path.
        job_details_extraction(url: str) -> dict: Extracts job details from the specified job URL.
        resume_builder(job_details: dict, user_data: dict) -> dict: Generates a resume based on job details and user data.
        cover_letter_generator(job_details: dict, user_data: dict) -> str: Generates a cover letter based on job details and user data.
        resume_cv_pipeline(job_url: str, user_data_path: str) -> None: Runs the Auto Apply Pipeline.
    """

    def __init__(
        self, api_key: str, provider: str, downloads_dir: str = utils.get_default_download_folder()
    ):

        if provider is None or provider.strip() == "":
            self.provider = "gemini"
        else:
            self.provider = provider

        if api_key is None or api_key.strip() == "os":
            if provider == "openai":
                self.api_key = os.environ.get("OPENAI_API_KEY")
            elif provider == "gemini":
                self.api_key = os.environ.get("GEMINI_API_KEY")
                print("===== GOT GEMINI API KEY ======")
        else:
            self.api_key = api_key

        if downloads_dir is None or downloads_dir.strip() == "":
            self.downloads_dir = utils.get_default_download_folder()
        else:
            self.downloads_dir = downloads_dir
    
    # Define a function to perform similarity search between user and job description
    def find_similar_points(self, user_embeddings, job_embeddings):
            try:
                relevant_points = set()
                for embedding in job_embeddings['embedding']:
                    dot_products = np.dot(np.stack(user_embeddings['embedding']), embedding)
                    idx = np.argmax(dot_products)
                    relevant_points.add(user_embeddings.iloc[idx]['chunk'])
                
                return relevant_points
            except Exception as e:      
                print(e)
                return None

    def resume_to_json(self, pdf_path):
        """
        Converts a resume in PDF format to JSON format.

        Args:
            pdf_path (str): The path to the PDF file.

        Returns:
            dict: The resume data in JSON format.
        """
        # TODO: Prompt Template
        system_prompt = utils.get_prompt(
            os.path.join(prompt_path, "resume-extractor.txt")
        )
        llm = self.get_llm_instance(system_prompt)
        resume_text = extract_text(pdf_path)
        resume_json = llm.get_response(resume_text, need_json_output=True)
        return resume_json
    
    def read_data_from_url(self, urls):
        try: 
            # loader = UnstructuredURLLoader(urls=urls, ssl_verify=False, remove_selectors=["header", "footer"])
            url_content = ""
            loader = PlaywrightURLLoader(urls=urls, remove_selectors=["header", "footer"])
            pages = loader.load()

            for page in pages:
                if page.page_content.strip() != "":
                    # text = page.extract_text().split("\n")
                    text_list = page.page_content.split("\n")

                    # Remove Unicode characters from each line
                    cleaned_texts = [re.sub(r'[^\x00-\x7F]+', '', line) for line in text_list]
                    cleaned_texts = [text.strip() for text in cleaned_texts if text.strip() not in ['', None]]

                    # Join the lines into a single string
                    cleaned_texts_string = '\n'.join(cleaned_texts)
                    url_content += cleaned_texts_string
                
                return url_content
        except Exception as e:
            print(e)
            return None
    
    def get_llm_instance(self, system_prompt):
        if self.provider == "openai":
            return ChatGPT(api_key=self.api_key, system_prompt=system_prompt)
        elif self.provider == "together":
            return TogetherAI(api_key=self.api_key, system_prompt=system_prompt)
        elif self.provider == "gemini":
            return Gemini(api_key=self.api_key, system_prompt=system_prompt)
        else:
            raise Exception("Invalid LLM Provider")

    @utils.measure_execution_time
    def user_data_extraction(self, user_data_path: str = demo_data_path, is_st=False):
        """
        Extracts user data from the given file path.

        Args:
            user_data_path (str): The path to the user data file.

        Returns:
            dict: The extracted user data in JSON format.
        """
        print("\nFetching user data...")

        if user_data_path is None or (type(user_data_path) is str and user_data_path.strip() == ""):
            user_data_path = demo_data_path


        # Read user data
        extension = os.path.splitext(user_data_path)[1]
        if extension == ".pdf":
            user_data = self.resume_to_json(user_data_path)
        elif extension == ".json":
            user_data = utils.read_json(user_data_path)
        elif validators.url(user_data_path):
            user_data = self.read_data_from_url([user_data_path])
            pass
        else:
            raise Exception("Invalid file format. Please provide a PDF, JSON file or url.")
        
        return user_data

    @utils.measure_execution_time
    def job_details_extraction(self, url: str=None, job_site_content: str=None, is_st=False):
        """
        Extracts job details from the specified job URL.

        Args:
            url (str): The URL of the job posting.
            job_site_content (str): The content of the job posting.

        Returns:
            dict: A dictionary containing the extracted job details.
        """
        
        print("\nExtracting job details...")

        try:
            system_prompt = utils.get_prompt(
                os.path.join(prompt_path, "persona-job-llm.txt")
            ) + utils.get_prompt(
                os.path.join(prompt_path, "extract-job-detail.txt")
            )

            # TODO: Handle case where it returns None. sometime, website take time to load, but scraper complete before that.
            if url is not None and url.strip() != "":
                job_site_content = get_url_content(url)
                if job_site_content is None:
                    raise Exception("Unable to web scrape the job description.")

            llm = self.get_llm_instance(system_prompt)
            job_details = llm.get_response(job_site_content, need_json_output=True)
            if url is not None and url.strip() != "":
                job_details["url"] = url
            jd_path = utils.job_doc_name(job_details, self.downloads_dir, "jd")

            utils.write_json(jd_path, job_details)
            print(f"Job Details JSON generated at: {jd_path}")

            if url is not None and url.strip() != "":
                del job_details['url']
            
            return job_details, jd_path

        except Exception as e:
            print(e)
            st.write("Please try pasting the job description text instead of the URL.")
            st.error(f"Error in Job Details Parsing, {e}")
            return None, None
 
    @utils.measure_execution_time
    def cover_letter_generator(self, job_details: dict, user_data: dict, need_pdf: bool = True, is_st=False):
        """
        Generates a cover letter based on the provided job details and user data.

        Args:
            job_details (dict): A dictionary containing the job description.
            user_data (dict): A dictionary containing the user's resume or work information.

        Returns:
            str: The generated cover letter.

        Raises:
            None
        """
        print("\nGenerating Cover Letter...")

        try:
            system_prompt = utils.get_prompt(
                os.path.join(prompt_path, "persona-job-llm.txt")
            ) + utils.get_prompt(
                os.path.join(prompt_path, "generate-cover-letter.txt")
            )
            query = f"""Provided Job description delimited by triple backticks(```) and \
                        my resume or work information below delimited by triple dashes(---).
                        ```
                        {json.dumps(job_details)}
                        ```

                        ---
                        {json.dumps(user_data)}
                        ---
                    """

            llm = self.get_llm_instance(system_prompt)
            cover_letter = llm.get_response(query, expecting_longer_output=True)
            cv_path = utils.job_doc_name(job_details, self.downloads_dir, "cv")
            utils.write_file(cv_path, cover_letter)
            print("Cover Letter generated at: ", cv_path)
            if need_pdf:
                utils.text_to_pdf(cover_letter, cv_path.replace(".txt", ".pdf"))
                print("Cover Letter PDF generated at: ", cv_path.replace(".txt", ".pdf"))
            
            return cover_letter, cv_path.replace(".txt", ".pdf")
        except Exception as e:
            print(e)
            st.write("Error: \n\n",e)
            return None, None


    @utils.measure_execution_time
    async def resume_builder(self, job_details: dict, user_data: dict, is_st=False):
        """
        Builds a resume based on the provided job details and user data.

        Args:
            job_details (dict): A dictionary containing the job description.
            user_data (dict): A dictionary containing the user's resume or work information.

        Returns:
            dict: The generated resume details.

        Raises:
            FileNotFoundError: If the system prompt files are not found.
        """
        try:
            print("\nGenerating Resume Details...")
            if is_st: st.toast("Generating Resume Details...")

            resume_details = dict()
            system_prompt = utils.get_prompt(os.path.join(prompt_path, "persona-job-llm.txt"))

            # Personal Information Section
            if is_st: st.toast("Processing Resume's Personal Info Section...")
            resume_details["personal"] = { 
                "name": user_data["name"], 
                "phone": user_data["phone"], 
                "email": user_data["email"],
                "github": user_data["media"]["github"], 
                "linkedin": user_data["media"]["linkedin"]
                }
            st.markdown("**Personal Info Section**")
            st.write(resume_details)

            sections = ['work_experience', 'skill_section', 'projects', 'education', 'certifications', 'achievements']
            async with aiohttp.ClientSession() as self.session:
                tasks = [self.process_section(section, user_data, job_details) for section in sections]
                results = await asyncio.gather(*tasks)

            resume_details = {}
            for result in results:
                resume_details.update(result)

            resume_details['keywords'] = job_details['keywords']
            
            resume_path = utils.job_doc_name(job_details, self.downloads_dir, "resume")

            utils.write_json(resume_path, resume_details)
            resume_path = resume_path.replace(".json", ".pdf")
            # st.write(f"resume_path: {resume_path}")

            resume_latex = latex_to_pdf(resume_details, resume_path)
            # st.write(f"resume_pdf_path: {resume_pdf_path}")

            return resume_path, resume_details
        except Exception as e:
            print(e)
            st.write("Error: \n\n",e)
            return resume_path, resume_details

    def resume_cv_pipeline(self, job_url: str, user_data_path: str = demo_data_path):
        """Run the Auto Apply Pipeline.

        Args:
            job_url (str): The URL of the job to apply for.
            user_data_path (str, optional): The path to the user profile data file.
                Defaults to os.path.join(module_dir, "master_data','user_profile.json").

        Returns:
            None: The function prints the progress and results to the console.
        """
        try:
            if user_data_path is None or user_data_path.strip() == "":
                user_data_path = demo_data_path

            print("Starting Auto Resume and CV Pipeline")
            if job_url is None and len(job_url.strip()) == "":
                print("Job URL is required.")
                return
            
            # Extract user data
            user_data = self.user_data_extraction(user_data_path)

            # Extract job details
            job_details, jd_path = self.job_details_extraction(url=job_url)
            # job_details = read_json("/Users/saurabh/Downloads/JobLLM_Resume_CV/Netflix/Netflix_MachineLearning_JD.json")

            # Build resume
            resume_path, resume_details = self.resume_builder(job_details, user_data)
            # resume_details = read_json("/Users/saurabh/Downloads/JobLLM_Resume_CV/Netflix/Netflix_MachineLearning_resume.json")
            
            # Generate cover letter
            cv_details, cv_path = self.cover_letter_generator(job_details, user_data)

            # Calculate metrics
            for metric in ['jaccard_similarity', 'overlap_coefficient', 'cosine_similarity']:
                print(f"\nCalculating {metric}...")

                if metric == 'vector_embedding_similarity':
                    llm = self.get_llm_instance('')
                    user_personlization = globals()[metric](llm, json.dumps(resume_details), json.dumps(user_data))
                    job_alignment = globals()[metric](llm, json.dumps(resume_details), json.dumps(job_details))
                    job_match = globals()[metric](llm, json.dumps(user_data), json.dumps(job_details))
                else:
                    user_personlization = globals()[metric](json.dumps(resume_details), json.dumps(user_data))
                    job_alignment = globals()[metric](json.dumps(resume_details), json.dumps(job_details))
                    job_match = globals()[metric](json.dumps(user_data), json.dumps(job_details))

                print("User Personlization Score(resume,master_data): ", user_personlization)
                print("Job Alignment Score(resume,JD): ", job_alignment)
                print("Job Match Score(master_data,JD): ", job_match)

            print("\nDone!!!")
        except Exception as e:
            print(e)
            return None

class AsyncResumeProcessor:
    def __init__(self, llm, utils, prompt_path, system_prompt, is_st):
        self.llm = llm
        self.utils = utils
        self.prompt_path = prompt_path
        self.system_prompt = system_prompt
        self.is_st = is_st
        self.session = None

    async def process_section(self, section: str, user_data: Dict[str, Any], job_details: Dict[str, Any]) -> Dict[str, Any]:
        section_log = f"Processing Resume's {section.upper()} Section..."
        if self.is_st:
            import streamlit as st
            st.toast(section_log)

        query = self.utils.get_prompt(os.path.join(self.prompt_path, "sections", f"{section}.txt"))
        query = query.replace("<SECTION_DATA>", json.dumps(user_data[section])).replace("<JOB_DESCRIPTION>", json.dumps(job_details))

        response = await self.llm.get_response_async(self.session, query, expecting_longer_output=True, need_json_output=True)

        result = {}
        if response is not None and isinstance(response, dict):
            if section in response:
                if response[section]:
                    if section == "skill_section":
                        result[section] = [i for i in response['skill_section'] if len(i['skills'])]
                    else:
                        result[section] = response[section]

        if self.is_st:
            import streamlit as st
            st.markdown(f"**{section.upper()} Section**")
            st.write(response)

        return {section: result.get(section, [])}