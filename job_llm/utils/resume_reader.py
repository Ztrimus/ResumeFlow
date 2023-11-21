import PyPDF2
import re
import json

class PDFResumeParser:
    def __init__(self):
        self.pdf_path = '../input/Amey_Bhilegaonkar_Resume.pdf'
        self.resume_text = None
        self.output_json_path = '../output/ameyBhilegaonkar.json'

    def extract_text(self):
        with open(self.pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            num_pages = len(pdf_reader.pages)

            for page_num in range(num_pages):
                page = pdf_reader.pages[page_num]
                text = page.extract_text().split("\n")

                # Remove Unicode characters from each line
                cleaned_text = [re.sub(r'[^\x00-\x7F]+', '', line) for line in text]

                # Join the lines into a single string
                cleaned_text_string = '\n'.join(cleaned_text)
                self.resume_text = cleaned_text_string

    def save_to_json(self):
        with open(self.output_json_path, 'w') as json_file:
            json.dump(self.resume_text, json_file, indent=2)

