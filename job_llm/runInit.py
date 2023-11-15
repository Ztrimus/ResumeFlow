'''
-----------------------------------------------------------------------
File: LLM.py
Creation Time: Nov 1st 2023 1:40 am
Author: Amey Bhilegaonkar
Developer Email: abhilega@asu.edu
Copyright (c) 2023 Amey Bhilegaonkar. All rights reserved | GitHub: ameygoes
-----------------------------------------------------------------------
'''

import openai
import sys
import openai
sys.path.append('../../')

from job_llm import config
from job_llm.utils.llm_models import ChatGPT
from job_llm.utils.data_extraction import get_link_content


system_prompt = open("../prompts/job-detail-extractor.txt").read().strip()