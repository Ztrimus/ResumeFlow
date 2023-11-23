import os
import time
import json
import shutil
from fpdf import FPDF
from datetime import datetime
import aspose.pdf as pdf
import subprocess

def write_file(file_path, data):
    """Writes the given data to the specified file.

    Args:
        file_path (str): The file path where the data will be written.
        data (str): The data to be written to the file.
    """    
    with open(file_path, 'w') as file:
         file.write(data)

def read_file(file_path):
    """Reads the contents of the specified file.

    Args:
        file_path (str): The file path of the file to be read.

    Returns:
        str: The contents of the file.
    """
    with open(file_path, 'r') as file:
        file_contents = file.read()
    return file_contents

def write_json(file_path, data):
    """Writes the given data to the specified file in JSON format.

    Args:
        file_path (str): The file path where the JSON data will be written.
        data (dict): The data to be written to the file in JSON format.
    """
    with open(file_path, 'w') as json_file:
            json.dump(data, json_file)

def read_json(file_path: str):
    """
    Reads and loads JSON data from the specified file path.

    Args:
        file_path (str): The path to the JSON file.

    Returns:
        dict: A dictionary containing the JSON data.
    """  
    with open(file_path) as json_file:
        return json.load(json_file)

def job_doc_name(job_details: dict):
     company_name = clean_string(job_details["company_name"])
     job_title = clean_string(job_details["title"])
     return "_".join([company_name, job_title])
     
def clean_string(text: str):
     return text.title().replace(" ", "").strip()

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
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt=text)
    pdf.output(file_path)

def tex_to_pdf(tex_file_path: str, pdf_file_path: str):
    # Call pdflatex to convert LaTeX to PDF
    subprocess.run(['pdflatex', tex_file_path])

    # Move the PDF file to the specified file path
    shutil.copyfile(tex_file_path.replace(".tex", "pdf"), pdf_file_path)

    for file_type in [".aux", ".log", ".out", ".pdf"]:
        file_path = tex_file_path.replace(".tex", file_type)
        if os.path.exists(file_path):
            os.remove(file_path)

def tex_to_pdf_aspose(tex_file_path: str, pdf_file_path: str):
    """Converts the given LaTeX file to a PDF file.

    Args:
        tex_file_path (str): The file path of the LaTeX file.
        pdf_file_path (str): The file path where the PDF file will be saved.
    """
    # Create an instance of TeXLoadOptions class
    load_options = pdf.TeXLoadOptions()

    # Load the input LaTeX file with the Document class
    doc = pdf.Document(tex_file_path, load_options)

    # Convert the LaTeX file to a PDF file
    doc.save(pdf_file_path)

if __name__ == "__main__":
    tex_file_path = "logs/resume.tex"
    pdf_file_path = "logs/resume.pdf"
    tex_to_pdf(tex_file_path, pdf_file_path)