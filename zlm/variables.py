'''
-----------------------------------------------------------------------
File: zlm/variables.py
Creation Time: Aug 18th 2024, 5:26 am
Author: Saurabh Zinjad
Developer Email: saurabhzinjad@gmail.com
Copyright (c) 2023-2024 Saurabh Zinjad. All rights reserved | https://github.com/Ztrimus
-----------------------------------------------------------------------
'''

from zlm.prompts.sections_prompt import EXPERIENCE, SKILLS, PROJECTS, EDUCATIONS, CERTIFICATIONS, ACHIEVEMENTS
from zlm.schemas.sections_schemas import Achievements, Certifications, Educations, Experiences, Projects, SkillSections

GPT_EMBEDDING_MODEL = "text-embedding-ada-002"
# text-embedding-3-large, text-embedding-3-small

GEMINI_EMBEDDING_MODEL = "models/text-embedding-004"
# models/embedding-001

OLLAMA_EMBEDDING_MODEL = "bge-m3"

DEFAULT_LLM_PROVIDER = "Gemini"
DEFAULT_LLM_MODEL = "gemini-1.5-flash"

LLM_MAPPING = {
    'GPT': {
        "api_env": "OPENAI_API_KEY",
        "model": ["gpt-4o", "gpt-4o-mini", "gpt-4-turbo", "gpt-4-1106-preview", "gpt-3.5-turbo"], 
    },
    'Gemini': {
        "api_env": "GEMINI_API_KEY",
        "model": ["gemini-1.5-flash", "gemini-1.5-flash-latest", "gemini-1.5-pro", "gemini-1.5-pro-latest", "gemini-1.5-pro-exp-0801"], # "gemini-1.0-pro", "gemini-1.0-pro-latest"
    },
    # 'Ollama': {
    #     "api_env": None,
    #     "model": ['llama3.1', 'llama3'],
    # }
}

section_mapping = {
    "work_experience": {"prompt":EXPERIENCE, "schema": Experiences},
    "skill_section": {"prompt":SKILLS, "schema": SkillSections},
    "projects": {"prompt":PROJECTS, "schema": Projects},
    "education": {"prompt":EDUCATIONS, "schema": Educations},
    "certifications": {"prompt":CERTIFICATIONS, "schema": Certifications},
    "achievements": {"prompt":ACHIEVEMENTS, "schema": Achievements},
}