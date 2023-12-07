# Streamlining Job Applications with LLM Automation Pipeline

<p align="center">
<!-- <img src="https://raw.githubusercontent.com/Ztrimus/job-llm/main/resources/auto_job_apply_workflow.png?token=GHSAT0AAAAAACHNE2LVFGFGEZTWLCOA5WOIZLRLEMA" alt="Auto Job Apply Pipeline" width="auto" height="500"> -->
  <img src="resources/auto_job_apply_workflow.png" alt="Auto Job Apply Pipeline" width="auto" height="500">
</p>

Project source can be downloaded from https://github.com/Ztrimus/job-llm.git

All other known bugs and fixes can be sent to following emails with the subject _"[BUG] JOB LLM"_. Reported bugs/fixes will be submitted to correction.

#### Author & Contributor List

-   [Saurabh Zinjad - Ztrimus](https://linkedin.com/in/saurabhzinjad) | szinjad@asu.edu
-   [Amey Bhilegaonkar - ameygoes](https://www.linkedin.com/in/amey-bhilegaonkar/) | abhilega@asu.edu

## Introduction:

### 1. Motivation: LLMs as Components in an ML Pipeline

Solving a task using machine learning methods requires a series of steps that often require large amounts of human effort or labor. Some examples of this are:

-   data collection
-   data curation or something similar
-   data augmentation, etc.

Furthermore there might be more steps after the training the ML model, such as evaluation, explaining the behavior of the model,
interpreting model outputs, etc. Many of these steps are also often human labor intensive. In this project, we will investigate how to effectively use Large Language Models (LLMs) to automate various aspects of this pipeline.

### 2. Our Proposal

We're aiming to create a automated system that makes applying for jobs a breeze. Job hunting has many stages, and we see a chance to automate things and use LLM (Language Model) to make it even smoother. We're looking at different ways, both the usual and some new ideas, to integrate LLM into the job application process. The goal is to reduce how much you have to do and let LLM do its thing, making the whole process easier for you.

### 3. Refer [Project Report](./resources/Project%20Report.pdf) for more details.

## Get Started and Setup

1. Prerequisites
    - OS - Linux (Ubuntu 22.04)
    - Python - 3.10.12
    - OpenAI API key - Store it in your environment variable called `OPENAI_API_KEY`. you can access it thorugh [config.py](./zlm/config.py).
2. Create and activate python environment (use `python -m venv .env` or conda or etc.) to avoid any package dependency conflict.
3. Install [Poetry package](https://python-poetry.org/docs/basic-usage/) (dependency management and packaging tool)
    ```bash
    pip install poetry
    ```
4. Install all required packages.
   4.1. Refer [pyproject.toml](pyproject.toml) or [poetry.lock](poetry.lock) for list of packages.
   `bash
poetry install
`
   OR
   4.2. We recommend using poetry, if above command not working, we also provided [requirements.txt](resources/requirements.txt) file.
   `bash
    pip install -r resources/requirements.txt
    `
5. on linux you also need to install following pakages to convert latex to pdf.
    ```bash
    sudo apt-get install texlive-latex-base texlive-fonts-recommended texlive-fonts-extra
    ```
    NOTE: try `sudo apt-get update` if terminal unable to locate package.

## Run Code

```bash
python main.py --url "JOB_POSTING_URL" --master_data="JSON_USER_MASTER_DATA"
```

-   Refer following example

```bash
python main.py --url "https://www.squarespace.com/careers/jobs/5369485?ref=Simplify" --master_data="master_data/user_profile.json"
```

## Usage as package

```bash
pip install zlm
```

```python
import os
from zlm import AutoApplyModel

job_llm = AutoApplyModel(os.environ['OPENAI_API_KEY'])
job_llm.resume_cv_pipeline("JOB_URL_HERE")
```

## References

-   [Overleaf LaTex Resume Template](https://www.overleaf.com/latex/templates/jakes-resume-anonymous/cstpnrbkhndn)
-   [Combining LaTeX with Python](https://tug.org/tug2019/slides/slides-ziegenhagen-python.pdf)
-   [OpenAI Documentation](https://platform.openai.com/docs/api-reference/chat/create)

## Limitation and Further growth :

## TODO:

-   Evaluation of generated resumes: metrics can be
    -   **Content Preservation**: overlap b/w keywords from resume and master data.
    -   **Goodness of resume for certain job**: Overlap b/w generated resume and job description.
-   Streamlit app development
-   When ship as package give option for
    -   Passing OPENAI_API_KEY
    -   Where to Download folder or path
