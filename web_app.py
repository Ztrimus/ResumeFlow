'''
-----------------------------------------------------------------------
File: app.py
Creation Time: Jan 30th 2024, 11:00 am
Author: Saurabh Zinjad
Developer Email: saurabhzinjad@gmail.com
Copyright (c) 2023-2024 Saurabh Zinjad. All rights reserved | https://github.com/Ztrimus
-----------------------------------------------------------------------
'''
import os
import json
import base64
import shutil
import subprocess
import streamlit as st

command = "apt install texlive-latex-base texlive-fonts-recommended texlive-fonts-extra"
process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
output, error = process.communicate()

from zlm import AutoApplyModel
from zlm.utils.metrics import jaccard_similarity, overlap_coefficient, cosine_similarity

def displayPDF(file):
    # Opening file from file path
    with open(file, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')

    # Embedding PDF in HTML
    pdf_display =  f"""<embed
    class="pdfobject"
    type="application/pdf"
    title="Embedded PDF"
    src="data:application/pdf;base64,{base64_pdf}"
    style="overflow: auto; width: 100%; height: 100vh">"""

    # Displaying File
    st.markdown(pdf_display, unsafe_allow_html=True)

st.set_page_config(
    page_title="Resume Generation!",
    page_icon="📑",
    menu_items={
        'About': 'https://github.com/Ztrimus/job-llm',
        'Report a bug': "https://github.com/Ztrimus/job-llm/issues",
    }
)

# st.markdown("<h1 style='text-align: center; color: grey;'>Get :green[Job Aligned] :orange[Killer] Resume :sunglasses:</h1>", unsafe_allow_html=True)
st.header("Get :green[Job Aligned] :orange[Personalized] Resume", divider='rainbow')
# st.subheader("Skip the writing, land the interview")

col_1, col_2 = st.columns(2)
with col_1:
    provider = st.selectbox("Select LLM provider([OpenAI](https://openai.com/blog/openai-api), [Gemini Pro](https://ai.google.dev/)):", ["gemini", "openai"])
with col_2:
    api_key = st.text_input("Enter API key:", type="password")
    if api_key == "":
        api_key = None

col_text, col_url,_,_ = st.columns(4)
with col_text:
    st.write("Job Description Text")
with col_url:
    is_url_button = st.toggle('Job URL', True)


if is_url_button:
    url = st.text_input("Enter job posting URL:", placeholder="Enter job posting URL here...", label_visibility="collapsed")
else:
    text = st.text_area("Paste job description text:", max_chars=5500, height=250, placeholder="Paste job description text here...", label_visibility="collapsed")

file = st.file_uploader("Upload your resume or work related data (json, pdf)", type=["json", "pdf"])
st.markdown("---") 

# Buttons side-by-side with styling
col1, col2, col3 = st.columns(3)
with col1:
    get_resume_button = st.button("Get Resume", key="get_resume", type="primary")

with col2:
    get_cover_letter_button = st.button("Get Cover Letter", key="get_cover_letter", type="primary")

with col3:
    get_both = st.button("Resume + Cover letter", key="both", type="primary")
    if get_both:
        get_resume_button = True
        get_cover_letter_button = True

if get_resume_button or get_cover_letter_button:
    if file is None:
        st.toast(":red[Upload user's resume or work related data to get started]", icon="⚠️")
    
    if url == "" and text == "":
        st.toast(":red[Please enter a job posting URL or paste the job description to get started]", icon="⚠️") 
    
    if file is not None and (url != "" or text != ""):
        resume_llm = AutoApplyModel(api_key=api_key, provider=provider, downloads_dir=None)
        
        # Save the uploaded file
        os.makedirs("uploads", exist_ok=True)
        file_path = os.path.abspath(os.path.join("uploads", file.name))
        with open(file_path, "wb") as f:
            f.write(file.getbuffer())
    
        # Extract user data
        user_data = resume_llm.user_data_extraction(file_path, is_st_print=True)
        st.write("Outer user_data: ", user_data)

        shutil.rmtree(os.path.dirname(file_path))

        # Extract job details
        if url != "":
            job_details = resume_llm.job_details_extraction(url=url, is_st_print=True)
        elif text != "":
            job_details = resume_llm.job_details_extraction(job_site_content=text, is_st_print=True)

        st.write("Outer Job Details: ", job_details)

        if job_details is not None:
            # Build Resume
            if get_resume_button:
                resume_path, resume_details = resume_llm.resume_builder(job_details, user_data, is_st_print=True)
                st.write("Outer resume_path: ", resume_path)
                st.write("Outer resume_details: ", resume_details)
                st.subheader("Generated Resume")
                
                # Calculate metrics
                st.subheader("Metrics")
                for metric in ['overlap_coefficient', 'cosine_similarity']:
                    user_personlization = globals()[metric](json.dumps(resume_details), json.dumps(user_data))
                    job_alignment = globals()[metric](json.dumps(resume_details), json.dumps(job_details))
                    job_match = globals()[metric](json.dumps(user_data), json.dumps(job_details))

                    if metric == "overlap_coefficient":
                        title = "Overlap Coefficient"
                        help_text = "The overlap coefficient is a measure of the overlap between two sets, and is defined as the size of the intersection divided by the smaller of the size of the two sets."
                    elif metric == "cosine_similarity":
                        title = "Cosine Similarity"
                        help_text = "The cosine similarity is a measure of the similarity between two non-zero vectors of an inner product space that measures the cosine of the angle between them."

                    st.caption(f"## **:rainbow[{title}]**", help=help_text)
                    col_m_1, col_m_2, col_m_3 = st.columns(3)
                    col_m_1.metric(label=":green[User Personlization Score]", value=f"{user_personlization:.3f}", delta="[resume,master_data]", delta_color="off")
                    col_m_2.metric(label=":blue[Job Alignment Score]", value=f"{job_alignment:.3f}", delta="[resume,JD]", delta_color="off")
                    col_m_3.metric(label=":violet[Job Match Score]", value=f"{job_match:.3f}", delta="[master_data,JD]", delta_color="off")

                displayPDF(resume_path)
                st.toast("Resume generated successfully!", icon="✅")
                st.markdown("---")

            # Build Cover Letter
            if get_cover_letter_button:
                cv_details, cv_pdf = resume_llm.cover_letter_generator(job_details, user_data, is_st_print=True)
                st.subheader("Generated Cover Letter")
                st.markdown("---")
                st.markdown(cv_details, unsafe_allow_html=True)
                st.toast("cover letter generated successfully!", icon="✅")
            
            st.toast(f"Done", icon="👍🏻")
            st.success(f"Done", icon="👍🏻")
            st.balloons()
            
            refresh = st.button("Refresh")

            if refresh:
                st.caching.clear_cache()
                st.rerun()
        else:
            st.error("Job details not able process. Please paste job description and try again.")
