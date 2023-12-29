'''
-----------------------------------------------------------------------
File: utils.py
Creation Time: Dec 6th 2023, 7:09 pm
Author: Saurabh Zinjad
Developer Email: zinjadsaurabh1997@gmail.com
Copyright (c) 2023 Saurabh Zinjad. All rights reserved | GitHub: Ztrimus
-----------------------------------------------------------------------
'''

import os
import re
import time
import json
import platform
import subprocess
from fpdf import FPDF
from pathlib import Path
from datetime import datetime
OS_SYSTEM = platform.system().lower()


def write_file(file_path, data):
    with open(file_path, "w") as file:
        file.write(data)


def read_file(file_path):
    with open(file_path, "r") as file:
        file_contents = file.read()
    return file_contents


def write_json(file_path, data):
    with open(file_path, "w") as json_file:
        json.dump(data, json_file, indent=2)


def read_json(file_path: str):
    with open(file_path) as json_file:
        return json.load(json_file)


def job_doc_name(job_details: dict, output_dir: str = "output", type: str = ""):
    company_name = clean_string(job_details["company_name"])
    job_title = clean_string(job_details["title"])[:15]
    doc_name = "_".join([company_name, job_title])
    doc_dir = os.path.join(output_dir, company_name)
    os.makedirs(doc_dir, exist_ok=True)

    if type == "jd":
        return os.path.join(doc_dir, f"{doc_name}_JD.json")
    elif type == "resume":
        return os.path.join(doc_dir, f"{doc_name}_resume.json")
    elif type == "cv":
        return os.path.join(doc_dir, f"{doc_name}_cv.txt")
    else:
        return os.path.join(doc_dir, f"{doc_name}_")


def clean_string(text: str):
    text = text.title().replace(" ", "").strip()
    text = re.sub(r"[^a-zA-Z0-9]+", "", text)
    return text

def open_file(file: str):
    if OS_SYSTEM == "darwin":  # macOS
        os.system(f"open {file}")
    elif OS_SYSTEM == "linux":
        try:
            os.system(f"xdg-open {file}")
        except FileNotFoundError:
            print("Error: xdg-open command not found. Please install xdg-utils.")
    elif OS_SYSTEM == "windows":
        try:
            os.startfile(file)
        except AttributeError:
            print("Error: os.startfile is not available on this platform.")
    else:
        # Default fallback for other systems
        try:
            os.system(f"xdg-open {file}")
        except FileNotFoundError:
            print(f"Error: xdg-open command not found. Please install xdg-utils. Alternatively, open the file manually.")


def save_log(content: any, file_name: str):
    timestamp = int(datetime.timestamp(datetime.now()))
    file_path = f"logs/{file_name}_{timestamp}.txt"
    write_file(file_path, content)


def measure_execution_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Function {func.__name__} took {execution_time:.4f} seconds to execute")
        return result

    return wrapper


def text_to_pdf(text: str, file_path: str):
    """Converts the given text to a PDF and saves it to the specified file path.

    Args:
        text (str): The text to be converted to PDF.
        file_path (str): The file path where the PDF will be saved.
    """
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=11)
    # Encode the text explicitly using 'latin-1' encoding
    encoded_text = text.encode('utf-8').decode('latin-1')
    pdf.multi_cell(0, 5, txt=encoded_text)
    pdf.output(file_path)
    # try:
    #     open_file(file_path)
    # except Exception as e:
    #     print("Unable to open the PDF file.")


def save_latex_as_pdf(tex_file_path: str, dst_path: str):
    # Call pdflatex to convert LaTeX to PDF
    prev_loc = os.getcwd()
    os.chdir(os.path.dirname(tex_file_path))
    result = subprocess.run(
        ["pdflatex", tex_file_path, "&>/dev/null"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    os.chdir(prev_loc)
    resulted_pdf_path = tex_file_path.replace(".tex", ".pdf")

    os.rename(resulted_pdf_path, dst_path)

    if result.returncode != 0:
        print("Exit-code not 0, check result!")
    try:
        open_file(dst_path)
    except Exception as e:
        print("Unable to open the PDF file.")

    filename_without_ext = os.path.basename(tex_file_path).split(".")[0]
    unnessary_files = [
        file
        for file in os.listdir(os.path.dirname(os.path.realpath(tex_file_path)))
        if file.startswith(filename_without_ext)
    ]
    for file in unnessary_files:
        file_path = os.path.join(os.path.dirname(tex_file_path), file)
        if os.path.exists(file_path):
            os.remove(file_path)

    with open(dst_path, "rb") as f:
        pdf_data = f.read()

    return pdf_data


def get_default_download_folder():
    """Get the default download folder for the current operating system."""

    if OS_SYSTEM == "windows":
        return os.path.join(str(Path.home()), "Downloads", "JobLLM_Resume_CV")
    elif OS_SYSTEM == "darwin":  # macOS
        return os.path.join(str(Path.home()), "Downloads", "JobLLM_Resume_CV")
    elif OS_SYSTEM == "linux":
        return os.path.join(str(Path.home()), "Downloads", "JobLLM_Resume_CV")
    else:
        # Default fallback for other systems
        return os.path.join(str(Path.home()), "Downloads", "JobLLM_Resume_CV")

def parse_json_markdown(json_string: str) -> dict:
    try:
        # Try to find JSON string within first and last triple backticks
        match = re.search(r"""```       # match first occuring triple backticks
                            (?:json)? # zero or one match of string json in non-capturing group
                            (.*)```   # greedy match to last triple backticks""", json_string, flags=re.DOTALL|re.VERBOSE)

        # If no match found, assume the entire string is a JSON string
        if match is None:
            json_str = json_string
        else:
            # If match found, use the content within the backticks
            json_str = match.group(1)

        # Strip whitespace and newlines from the start and end
        json_str = json_str.strip()

        # Parse the JSON string into a Python dictionary while allowing control characters by setting strict to False
        parsed = json.loads(json_str, strict=False)

        return parsed
    except Exception as e:
        print(e)
        return None

def get_system_prompt(system_prompt_path: str) -> str:
        """
        Reads the content of the file at the given system_prompt_path and returns it as a string.

        Args:
            system_prompt_path (str): The path to the system prompt file.

        Returns:
            str: The content of the file as a string.
        """
        with open(system_prompt_path, encoding="utf-8") as file:
            return file.read().strip() + "\n"
