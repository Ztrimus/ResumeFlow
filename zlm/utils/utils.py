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
import time
import json
import platform
import subprocess
from fpdf import FPDF
from pathlib import Path
from datetime import datetime


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
    return text.title().replace(" ", "").strip()


def open_file(file: str):
    os.system(f"browse {file}")


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
    pdf.multi_cell(0, 5, txt=text)
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
    system = platform.system().lower()

    if system == "windows":
        return os.path.join(str(Path.home()), "Downloads", "JobLLM_Resume_CV")
    elif system == "darwin":  # macOS
        return os.path.join(str(Path.home()), "Downloads", "JobLLM_Resume_CV")
    elif system == "linux":
        return os.path.join(str(Path.home()), "Downloads", "JobLLM_Resume_CV")
    else:
        # Default fallback for other systems
        return os.path.join(str(Path.home()), "Downloads", "JobLLM_Resume_CV")
