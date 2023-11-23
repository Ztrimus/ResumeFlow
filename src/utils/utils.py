import time
import json
from fpdf import FPDF
from datetime import datetime

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