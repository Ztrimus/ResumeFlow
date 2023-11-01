'''
-----------------------------------------------------------------------
File: demo.py
Creation Time: Nov 1st 2023 3:08 am
Author: Saurabh Zinjad
Developer Email: zinjadsaurabh1997@gmail.com
Copyright (c) 2023 Saurabh Zinjad. All rights reserved | GitHub: Ztrimus
-----------------------------------------------------------------------
'''

from job_llm import config
from job_llm.utils.llm_models import ChatGPT
from job_llm.utils.data_extraction import get_link_content

def main():
    system_prompt = open("./job_llm/prompts/job-detail-extractor.txt").read().strip()
    web_content_prompt = get_link_content("https://www.linkedin.com/jobs/view/3749167580")

    chat_gpt = ChatGPT(openai_api_key=config.OPENAI_API_KEY, system_prompt=system_prompt)
    response = chat_gpt.get_response(web_content_prompt)

    with open("demo-result.txt", 'w') as file:
        file.write(response)
    
    print(response)

if __name__ == "__main__":
    main()