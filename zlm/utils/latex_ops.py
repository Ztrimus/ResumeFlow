'''
-----------------------------------------------------------------------
File: latex_ops.py
Creation Time: Nov 24th 2023 3:29 am
Author: Saurabh Zinjad
Developer Email: zinjadsaurabh1997@gmail.com
Copyright (c) 2023 Saurabh Zinjad. All rights reserved | GitHub: Ztrimus
-----------------------------------------------------------------------
'''

import jinja2
import os
from zlm.utils.utils import write_file, save_latex_as_pdf

def escape_for_latex(data):
    if isinstance(data, dict):
        new_data = {}
        for key in data.keys():
            new_data[key] = escape_for_latex(data[key])
        return new_data
    elif isinstance(data, list):
        return [escape_for_latex(item) for item in data]
    elif isinstance(data, str):
        # Adapted from https://stackoverflow.com/q/16259923
        latex_special_chars = {
            "&": r"\&",
            "%": r"\%",
            "$": r"\$",
            "#": r"\#",
            "_": r"\_",
            "{": r"\{",
            "}": r"\}",
            "~": r"\textasciitilde{}",
            "^": r"\^{}",
            "\\": r"\textbackslash{}",
            "\n": "\\newline%\n",
            "-": r"{-}",
            "\xA0": "~",  # Non-breaking space
            "[": r"{[}",
            "]": r"{]}",
        }
        return "".join([latex_special_chars.get(c, c) for c in data])

    return data

def latex_to_pdf(json_resume, dst_path):
    try:
        module_dir = os.path.dirname(__file__)
        templates_path = os.path.join(module_dir, '..', 'templates')

        latex_jinja_env = jinja2.Environment(
            block_start_string="\BLOCK{",
            block_end_string="}",
            variable_start_string="\VAR{",
            variable_end_string="}",
            comment_start_string="\#{",
            comment_end_string="}",
            line_statement_prefix="%-",
            line_comment_prefix="%#",
            trim_blocks=True,
            autoescape=False,
            loader=jinja2.FileSystemLoader(templates_path),
        )

        escaped_json_resume = escape_for_latex(json_resume)

        resume_latex = use_template(latex_jinja_env, escaped_json_resume)
        tex_temp_path = os.path.join(os.path.realpath(templates_path), os.path.basename(dst_path).replace(".pdf", ".tex"))
        write_file(tex_temp_path, resume_latex)
        return save_latex_as_pdf(tex_temp_path, dst_path)
    except Exception as e:
        print(e)
        return None

def use_template(jinja_env, json_resume):
    try:
        resume_template = jinja_env.get_template(f"resume.tex.jinja")
        resume = resume_template.render(json_resume)

        return resume
    except Exception as e:
        print(e)
        return None
