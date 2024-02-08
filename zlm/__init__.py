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
import time
import streamlit as st

import numpy as np

from zlm.utils.llm_models import ChatGPT, Gemini, TogetherAI
from zlm.utils.data_extraction import get_url_content, extract_text
from zlm.utils.latex_ops import latex_to_pdf
from zlm.utils.utils import (
    get_default_download_folder,
    key_value_chunking,
    measure_execution_time,
    read_json,
    write_file,
    write_json,
    job_doc_name,
    text_to_pdf,
    get_prompt,
)
from zlm.utils.metrics import jaccard_similarity, overlap_coefficient, cosine_similarity, vector_embedding_similarity


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
        self, api_key: str, provider: str, downloads_dir: str = get_default_download_folder()
    ):

        if provider is None or provider.strip() == "":
            self.provider = "openai"
        else:
            self.provider = provider

        if api_key is None or api_key.strip() == "os":
            if provider == "openai":
                self.api_key = os.environ.get("OPENAI_API_KEY")
            elif provider == "together":
                self.api_key = os.environ.get("TOGETHER_KEY")
            elif provider == "gemini":
                self.api_key = os.environ.get("GEMINI_API_KEY")
        else:
            self.api_key = api_key

        if downloads_dir is None or downloads_dir.strip() == "":
            self.downloads_dir = get_default_download_folder()
        else:
            self.downloads_dir = downloads_dir
    
    # def load_and_split_documents(self, data, chunk_size=1024, chunk_overlap=100):
    #     try:
    #         # DO: Decide apt chunk size and overlap. start small(128/256) for granular semnatic info to large(512/1024) chunks for broad context.
    #         text_splitter = RecursiveCharacterTextSplitter(
    #             chunk_size=chunk_size, 
    #             chunk_overlap=chunk_overlap,
    #             length_function=len
    #         )
    #         chunks = text_splitter.split_text(data)
    #         return chunks
    #     except Exception as e:
    #         print(e)
    #         return None
    
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

        # similar_points = []
        # for i, doc_embedding in enumerate(document_embeddings):
        #     similarity_score = openai.Similarity(
        #         documents=[query_embedding, doc_embedding],
        #         model="text-davinci-003-001"
        #     )
        #     if similarity_score > 0.8:  # Adjust the threshold as per your requirement
        #         similar_points.append(document[i])
        # return similar_points
            
        # qa = RetrievalQA(vector_store=user_embeddings, query_vector_store=job_embeddings, k=3)

    def resume_to_json(self, pdf_path):
        """
        Converts a resume in PDF format to JSON format.

        Args:
            pdf_path (str): The path to the PDF file.

        Returns:
            dict: The resume data in JSON format.
        """
        system_prompt = get_prompt(
            os.path.join(prompt_path, "resume-extractor.txt")
        )
        llm = self.get_llm_instance(system_prompt)
        resume_text = extract_text(pdf_path)
        resume_json = llm.get_response(resume_text, need_json_output=True)
        return resume_json
    
    def get_llm_instance(self, system_prompt):
        if self.provider == "openai":
            return ChatGPT(api_key=self.api_key, system_prompt=system_prompt)
        elif self.provider == "together":
            return TogetherAI(api_key=self.api_key, system_prompt=system_prompt)
        elif self.provider == "gemini":
            return Gemini(api_key=self.api_key, system_prompt=system_prompt)
        else:
            raise Exception("Invalid LLM Provider")

    @measure_execution_time
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
        if os.path.splitext(user_data_path)[1] == ".pdf":
            user_data = self.resume_to_json(user_data_path)
        else:
            user_data = read_json(user_data_path)
        
        return user_data

    @measure_execution_time
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
            system_prompt = get_prompt(
                os.path.join(prompt_path, "persona-job-llm.txt")
            ) + get_prompt(
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
            jd_path = job_doc_name(job_details, self.downloads_dir, "jd")

            write_json(jd_path, job_details)
            print(f"Job Details JSON generated at: {jd_path}")

            if url is not None and url.strip() != "":
                del job_details['url']
            
            return job_details, jd_path

        except Exception as e:
            print(e)
            return None
 
    @measure_execution_time
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

        system_prompt = get_prompt(
            os.path.join(prompt_path, "persona-job-llm.txt")
        ) + get_prompt(
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
        cv_path = job_doc_name(job_details, self.downloads_dir, "cv")
        write_file(cv_path, cover_letter)
        print("Cover Letter generated at: ", cv_path)
        if need_pdf:
            text_to_pdf(cover_letter, cv_path.replace(".txt", ".pdf"))
            print("Cover Letter PDF generated at: ", cv_path.replace(".txt", ".pdf"))
        
        return cover_letter, cv_path.replace(".txt", ".pdf")


    @measure_execution_time
    def resume_builder(self, job_details: dict, user_data: dict, is_st=False):
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
            system_prompt = get_prompt(os.path.join(prompt_path, "persona-job-llm.txt"))

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

            # Other Sections
            for section in ['work', 'education', 'skill_section', 'projects', 'certifications', 'achievements']:
                section_log = f"Processing Resume's {section.upper()} Section..."
                if is_st: st.toast(section_log)
                query = get_prompt(os.path.join(prompt_path, "sections", f"{section}.txt"))
                query = query.replace("<SECTION_DATA>", json.dumps(user_data[section])).replace("<JOB_DESCRIPTION>", json.dumps(job_details))

                llm = self.get_llm_instance(system_prompt)
                response = llm.get_response(query, expecting_longer_output=True, need_json_output=True)
                resume_details[section] = response[section]
                
                if is_st:
                    st.markdown(f"**{section.upper()} Section**")
                    st.write(response)

            resume_details['keywords'] = job_details['keywords']
            
            resume_path = job_doc_name(job_details, self.downloads_dir, "resume")

            write_json(resume_path, resume_details)
            resume_path = resume_path.replace(".json", ".pdf")
            # st.write(f"resume_path: {resume_path}")

            resume_pdf_path, resume_latex = latex_to_pdf(resume_details, resume_path)
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

            # Generate cover letter
            cv_details, cv_path = self.cover_letter_generator(job_details, user_data)

            # Build resume
            resume_path, resume_details = self.resume_builder(job_details, user_data)
            # resume_details = read_json("/Users/saurabh/Downloads/JobLLM_Resume_CV/Netflix/Netflix_MachineLearning_resume.json")

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