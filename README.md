# ResumeFlow: An LLM-facilitated Pipeline for Personalized Resume Generation and Refinement 

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub issues open](https://img.shields.io/github/issues/Ztrimus/job-llm.svg?)](https://github.com/Ztrimus/job-llm/issues)

<img src="https://github.com/Ztrimus/job-llm/blob/main/resources/auto_job_apply_workflow.jpg" alt="Auto Job Aligned Personalized Resume Generation Pipeline" width="auto">
Auto Job Aligned Personalized Resume Generation Pipeline

Project source can be:
 - access as Web Tool from https://job-aligned-resume.streamlit.app/
 - Install as Python Package from https://pypi.org/project/zlm/
 - download from https://github.com/Ztrimus/job-llm.git

All other known bugs and fixes can be sent to following emails with the subject _"[BUG] JOB LLM"_. Reported bugs/fixes will be submitted to correction.

#### Author & Contributor List

 - [Saurabh Zinjad](https://linkedin.com/in/saurabhzinjad) | [Ztrimus](https://github.com/Ztrimus) | szinjad@asu.edu
 - [Amey Bhilegaonkar](https://www.linkedin.com/in/amey-bhilegaonkar) | [ameygoes](https://github.com/ameygoes) | abhilega@asu.edu
 - [Amrita Bhattacharjee](https://www.linkedin.com/in/amritabh) | [Amritabh](https://github.com/Amritabh) | abhatt43@asu.edu

## 1. Introduction:

### 1.1. Motivation: LLMs as Components in an ML Pipeline

In this project, we will investigate how to effectively use Large Language Models (LLMs) to automate various aspects of this pipeline.

Because, Solving a task using machine learning methods requires a series of steps that often require large amounts of human effort or labor. Furthermore there might be more steps after the training the ML model, such as evaluation, explaining the behavior of the model, interpreting model outputs, etc. Many of these steps are also often human labor intensive.

### 1.2. Our Proposal

We're aiming to create a automated system that makes applying for jobs a breeze. Job hunting has many stages, and we see a chance to automate things and use LLM (Language Model) to make it even smoother. We're looking at different ways, both the usual and some new ideas, to integrate LLM into the job application process. The goal is to reduce how much you have to do and let LLM do its thing, making the whole process easier for you.

### 1.3. Refer [Project Report](./resources/Project%20Report.pdf) for more details.

## 2. Setup, Installation and Usage

### 2.1. Prerequisites

 - OS : Linux, Mac
 - Python : 3.11.6 and above
 - LLM API key: [OpenAI](https://openai.com/pricing) OR [Gemini Pro](https://ai.google.dev/)

### 2.2. Package Installation - Use as Library

```bash
pip install zlm
```

 - Usage

```python
from zlm import AutoApplyModel

job_llm = AutoApplyModel(
    api_key="PROVIDE_API_KEY", 
    provider="ENTER PROVIDER <gemini> or <openai>",
    downloads_dir="[optional] ENTER FOLDER PATH WHERE FILE GET DOWNLOADED, By default, 'downloads' folder"
)

job_llm.resume_cv_pipeline(
    "ENTER_JOB_URL", 
    "YOUR_MASTER_RESUME_DATA" # .pdf or .json
) # Return and downloads curated resume and cover letter.
```

### 2.4. Setup & Run Code - Use as Project

```sh
git clone https://github.com/Ztrimus/job-llm.git
cd job-llm
```
 1. Create and activate python environment (use `python -m venv .env` or conda or etc.) to avoid any package dependency conflict.
 2. Install [Poetry package](https://python-poetry.org/docs/basic-usage/) (dependency management and packaging tool)
    ```bash
    pip install poetry
    ```
 3. Install all required packages.
     - Refer [pyproject.toml](pyproject.toml) or [poetry.lock](poetry.lock) for list of packages.
        ```bash
        poetry install
        ```
        OR
     - If above command not working, we also provided [requirements.txt](resources/requirements.txt) file. But, we recommend using poetry.
        ```bash
        pip install -r resources/requirements.txt
        ```
4. We also need to install following packages to conversion of latex to pdf
    - For linux
        ```bash
        sudo apt-get install texlive-latex-base texlive-fonts-recommended texlive-fonts-extra
        ```
        NOTE: try `sudo apt-get update` if terminal unable to locate package.
    - For Mac
        ```bash
        brew install basictex
        sudo tlmgr install enumitem fontawesome
        ```
5. Run following script to get result
```bash
>>> python main.py /
    --url "JOB_POSTING_URL" /
    --master_data="JSON_USER_MASTER_DATA" /
    --api_key="YOUR_LLM_PROVIDER_API_KEY" / # put api_key considering provider
    --downloads_dir="DOWNLOAD_LOCATION_FOR_RESUME_CV" /
    --provider="openai" # openai, gemini, together, g4f
```
## 3. References
 - [Prompt engineering Guidelines](https://platform.openai.com/docs/guides/prompt-engineering)
 - [Overleaf LaTex Resume Template](https://www.overleaf.com/latex/templates/jakes-resume-anonymous/cstpnrbkhndn)
 - [Combining LaTeX with Python](https://tug.org/tug2019/slides/slides-ziegenhagen-python.pdf)
 - [OpenAI Documentation](https://platform.openai.com/docs/api-reference/chat/create)

## 4. Limitation and Further growth :
 - ~~Evaluation of generated resumes: metrics can be~~
     - ~~**Content Preservation**: overlap b/w keywords from resume and master data.~~
     - ~~**Goodness of resume for certain job**: Overlap b/w generated resume and job description.~~
 - ~~Streamlit app development~~
 - ~~When ship as package give option for~~
     - ~~Passing OPENAI_API_KEY~~
     - ~~Where to Download folder or path~~