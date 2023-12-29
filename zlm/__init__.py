"""
-----------------------------------------------------------------------
File: auto_apply_model.py
Creation Time: Nov 21st 2023 2:49 am
Author: Saurabh Zinjad
Developer Email: zinjadsaurabh1997@gmail.com
Copyright (c) 2023 Saurabh Zinjad. All rights reserved | GitHub: Ztrimus
-----------------------------------------------------------------------
"""
import os
import json

import numpy as np

from zlm.utils.llm_models import ChatGPT, Gemini, TogetherAI
from zlm.utils.data_extraction import get_url_content, extract_text
from zlm.utils.latex_ops import latex_to_pdf
from zlm.utils.utils import (
    get_default_download_folder,
    measure_execution_time,
    read_json,
    write_file,
    write_json,
    job_doc_name,
    text_to_pdf,
    get_system_prompt
)
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS


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
        get_system_prompt(system_prompt_path: str) -> str: Returns the system prompt from the specified path.
        get_resume_to_json(pdf_path: str) -> dict: Extracts resume details from the specified PDF path.
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
    
    def load_and_split_documents(self, data, chunk_size=1024, chunk_overlap=100):
        try:
            # TODO: Decide apt chunk size and overlap. start small(128/256) for granular semnatic info to large(512/1024) chunks for broad context.
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=chunk_size, 
                chunk_overlap=chunk_overlap,
                length_function=len
            )
            chunks = text_splitter.split_text(data)
            return chunks
        except Exception as e:
            print(e)
            return None
    
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

    def get_resume_to_json(self, pdf_path):
        """
        Converts a resume in PDF format to JSON format.

        Args:
            pdf_path (str): The path to the PDF file.

        Returns:
            dict: The resume data in JSON format.
        """
        system_prompt = get_system_prompt(
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
    def user_data_extraction(self, user_data_path: str = demo_data_path):
        """
        Extracts user data from the given file path.

        Args:
            user_data_path (str): The path to the user data file.

        Returns:
            dict: The extracted user data in JSON format.
        """
        print("\nFetching User data...")

        if user_data_path is None or user_data_path.strip() == "":
            user_data_path = demo_data_path

        # Read user data
        if os.path.splitext(user_data_path)[1] == ".pdf":
            user_data = self.get_resume_to_json(user_data_path)
        else:
            user_data = read_json(user_data_path)
        
        # TODO: https://www.pinecone.io/learn/chunking-strategies/
        # langchain.text_splitter, Recursive Chunking, NLTKTextSplitter(), SpaCyTextSplitter(), 
        chunks = self.load_and_split_documents(json.dumps(user_data))

        # Create user embeddings
        llm = self.get_llm_instance("")
        vector_embedding = llm.get_embedding(chunks, task_type="retrieval_document")
        
        return user_data, vector_embedding

    @measure_execution_time
    def job_details_extraction(self, url: str=None, job_site_content: str=None):
        """
        Extracts job details from the specified job URL.

        Args:
            url (str): The URL of the job posting.
            job_site_content (str): The content of the job posting.

        Returns:
            dict: A dictionary containing the extracted job details.
        """
        
        print("\nExtracting Job Details...")

        try:
            system_prompt = get_system_prompt(
                os.path.join(prompt_path, "persona-job-llm.txt")
            ) + get_system_prompt(
                os.path.join(prompt_path, "extract-job-detail.txt")
            )

            # TODO: Handle case where it returns None. sometime, website take time to load, but scraper complete before that.
            if url is not None and url.strip() != "":
                job_site_content = get_url_content(url)
                while job_site_content is None:
                    job_site_content = get_url_content(url)

            llm = self.get_llm_instance(system_prompt)
            job_details = llm.get_response(job_site_content, need_json_output=True)
            # job_details = read_json("/Users/saurabh/Downloads/JobLLM_Resume_CV/Microsoft/Microsoft_ResearchInternG_JD.json")

            # Create user embeddings
            chunks = self.load_and_split_documents(json.dumps(job_details))
            vector_embedding = llm.get_embedding(chunks, task_type="retrieval_query")

            job_details["url"] = url
            jd_path = job_doc_name(job_details, self.downloads_dir, "jd")
            write_json(jd_path, job_details)
            print("Job Details JSON generated at: ", jd_path)
            return job_details, vector_embedding

        except Exception as e:
            print(e)
            return None
 
    @measure_execution_time
    def cover_letter_generator(self, job_details: dict, user_data: dict, need_pdf: bool = True):
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

        system_prompt = get_system_prompt(
            os.path.join(prompt_path, "persona-job-llm.txt")
        ) + get_system_prompt(
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
        
        return cv_path


    @measure_execution_time
    def resume_builder(self, job_details: dict, user_data: dict):
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

        print("\nGenerating Resume Details...")

        system_prompt = get_system_prompt(
            os.path.join(prompt_path, "persona-job-llm.txt")
        ) + get_system_prompt(
            os.path.join(prompt_path, "generate-resume-details.txt")
        )
        query = f"""Provided Job description delimited by triple backticks(```) and my resume or work information below delimited by triple dashes(---). ```{json.dumps(job_details)}``` ---{json.dumps(user_data)}---"""

        llm = self.get_llm_instance(system_prompt)
        resume_details = llm.get_response(query, expecting_longer_output=True, need_json_output=True)
        resume_details['keywords'] = job_details['keywords']
        resume_path = job_doc_name(job_details, self.downloads_dir, "resume")

        write_json(resume_path, resume_details)

        resume_path = resume_path.replace(".json", ".pdf")

        latex_to_pdf(resume_details, resume_path)
        print("Resume PDF generated at: ", resume_path)
        return resume_path

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

            user_data, user_embeddings = self.user_data_extraction(user_data_path)

            job_details, job_embeddings = self.job_details_extraction(url=job_url)

            relevant_points = self.find_similar_points(user_embeddings, job_embeddings)
            
            # TODO: Pass relevant points instad of user_data, but work on chunk strategies first.
            self.cover_letter_generator(job_details, user_data)

            self.resume_builder(job_details, user_data)

            print("Done!!!")
        except Exception as e:
            print(e)
            return None
