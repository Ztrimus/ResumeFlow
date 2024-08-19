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
import zipfile
import streamlit as st

from zlm import AutoApplyModel
from zlm.utils.utils import display_pdf, download_pdf, read_file, read_json
from zlm.utils.metrics import jaccard_similarity, overlap_coefficient, cosine_similarity
from zlm.variables import LLM_MAPPING

os.system("playwright install")

st.set_page_config(
    page_title="Resume Generator",
    page_icon="📑",
    menu_items={
        'Get help': 'https://www.youtube.com/watch?v=Agl7ugyu1N4',
        'About': 'https://github.com/Ztrimus/job-llm',
        'Report a bug': "https://github.com/Ztrimus/job-llm/issues",
    }
)

if os.path.exists("output"):
    shutil.rmtree("output")

def encode_tex_file(file_path):
    try:
        current_loc = os.path.dirname(__file__)
        print(f"current_loc: {current_loc}")
        file_paths = [file_path.replace('.pdf', '.tex'), os.path.join(current_loc, 'zlm', 'templates', 'resume.cls')]
        zip_file_path = file_path.replace('.pdf', '.zip')

        # Create a zip file
        with zipfile.ZipFile(zip_file_path, 'w') as zipf:
            for file_path in file_paths:
                zipf.write(file_path, os.path.basename(file_path))

        # Read the zip file content as bytes
        with open(zip_file_path, 'rb') as zip_file:
            zip_content = zip_file.read()

        # Encode the data using Base64
        encoded_zip = base64.b64encode(zip_content).decode('utf-8')

        return encoded_zip
    
    except Exception as e:
        st.error(f"An error occurred while encoding the file: {e}")
        print(e)
        return None

def create_overleaf_button(resume_path):
    tex_content = encode_tex_file(resume_path)
    html_code = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Overleaf Button</title>
        <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body style="background: transparent;">
        <div style="max-height: 30px !important;">
            <form action="https://www.overleaf.com/docs" method="post" target="_blank" height="20px">
                <input type="text" name="snip_uri" style="display: none;"
                    value="data:application/zip;base64,{tex_content}">
                <input class="btn btn-success rounded-pill w-100" type="submit" value="Edit in Overleaf 🍃">
            </form>
        </div>
        <!-- Bootstrap JS and dependencies -->
        <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.11.8/dist/umd/popper.min.js"></script>
        <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
    </body>
    </html>
    """
    st.components.v1.html(html_code, height=40)

try:
    # st.markdown("<h1 style='text-align: center; color: grey;'>Get :green[Job Aligned] :orange[Killer] Resume :sunglasses:</h1>", unsafe_allow_html=True)
    st.header("Get :green[Job Aligned] :orange[Personalized] Resume", divider='rainbow')
    # st.subheader("Skip the writing, land the interview")

    col_text, col_url,_,_ = st.columns(4)
    with col_text:
        st.write("Job Description Text")
    with col_url:
        is_url_button = st.toggle('Job URL', False)

    url, text = "", ""
    if is_url_button:
        url = st.text_input("Enter job posting URL:", placeholder="Enter job posting URL here...", label_visibility="collapsed")
    else:
        text = st.text_area("Paste job description text:", max_chars=5500, height=200, placeholder="Paste job description text here...", label_visibility="collapsed")

    file = st.file_uploader("Upload your resume or any work-related data(PDF, JSON). [Recommended templates](https://github.com/Ztrimus/job-llm/tree/main/zlm/demo_data)", type=["json", "pdf"])

    col_1, col_2, col_3 = st.columns(3)
    with col_1:
        provider = st.selectbox("Select provider([OpenAI](https://openai.com/blog/openai-api), [Gemini Pro](https://ai.google.dev/)):", LLM_MAPPING.keys())
    with col_2:
        model = st.selectbox("Select model:", LLM_MAPPING[provider]['model'])
    with col_3:
        if provider != "Ollama":
            api_key = st.text_input("Enter API key:", type="password", value="")
        else:
            api_key = None
    st.markdown("<sub><sup>💡 GPT-4 is recommended for better results.</sup></sub>", unsafe_allow_html=True)

    # Buttons side-by-side with styling
    col1, col2, col3 = st.columns(3)
    with col1:
        get_resume_button = st.button("Get Resume", key="get_resume", type="primary", use_container_width=True)

    with col2:
        get_cover_letter_button = st.button("Get Cover Letter", key="get_cover_letter", type="primary", use_container_width=True)

    with col3:
        get_both = st.button("Resume + Cover letter", key="both", type="primary", use_container_width=True)
        if get_both:
            get_resume_button = True
            get_cover_letter_button = True

    if get_resume_button or get_cover_letter_button:
        if file is None:
            st.toast(":red[Upload user's resume or work related data to get started]", icon="⚠️")
            st.stop()
        
        if url == "" and text == "":
            st.toast(":red[Please enter a job posting URL or paste the job description to get started]", icon="⚠️") 
            st.stop()
        
        if api_key == "" and provider != "Llama":
            st.toast(":red[Please enter the API key to get started]", icon="⚠️")
            st.stop()
        
        if file is not None and (url != "" or text != ""):
            download_resume_path = os.path.join(os.path.dirname(__file__), "output")

            resume_llm = AutoApplyModel(api_key=api_key, provider=provider, model = model, downloads_dir=download_resume_path)
            
            # Save the uploaded file
            os.makedirs("uploads", exist_ok=True)
            file_path = os.path.abspath(os.path.join("uploads", file.name))
            with open(file_path, "wb") as f:
                f.write(file.getbuffer())
        
            # Extract user data
            with st.status("Extracting user data..."):
                user_data = resume_llm.user_data_extraction(file_path, is_st=True)
                st.write(user_data)

            shutil.rmtree(os.path.dirname(file_path))

            if user_data is None:
                st.error("User data not able process. Please upload a valid file")
                st.markdown("<h3 style='text-align: center;'>Please try again</h3>", unsafe_allow_html=True)
                st.stop()

            # Extract job details
            with st.status("Extracting job details..."):
                if url != "":
                    job_details, jd_path = resume_llm.job_details_extraction(url=url, is_st=True)
                elif text != "":
                    job_details, jd_path = resume_llm.job_details_extraction(job_site_content=text, is_st=True)
                st.write(job_details)

            if job_details is None:
                st.error("Please paste job description. Job details not able process.")
                st.markdown("<h3 style='text-align: center;'>Please paste job description text and try again!</h3>", unsafe_allow_html=True)
                st.stop()

            # Build Resume
            if get_resume_button:
                with st.status("Building resume..."):
                    resume_path, resume_details = resume_llm.resume_builder(job_details, user_data, is_st=True)
                    # st.write("Outer resume_path: ", resume_path)
                    # st.write("Outer resume_details is None: ", resume_details is None)
                resume_col_1, resume_col_2, resume_col_3 = st.columns([0.35, 0.3, 0.25])
                with resume_col_1:
                    st.subheader("Generated Resume")
                with resume_col_2:
                    pdf_data = read_file(resume_path, "rb")

                    st.download_button(label="Download Resume ⬇",
                                        data=pdf_data,
                                        file_name=os.path.basename(resume_path),
                                        # on_click=download_pdf(resume_path),
                                        key="download_pdf_button",
                                        mime="application/pdf",
                                        use_container_width=True)
                with resume_col_3:
                    # Create and display "Edit in Overleaf" button
                    create_overleaf_button(resume_path)
                
                display_pdf(resume_path, type="image")
                st.toast("Resume generated successfully!", icon="✅")
                # Calculate metrics
                st.subheader("Resume Metrics")
                for metric in ['overlap_coefficient', 'cosine_similarity']:
                    user_personalization = globals()[metric](json.dumps(resume_details), json.dumps(user_data))
                    job_alignment = globals()[metric](json.dumps(resume_details), json.dumps(job_details))
                    job_match = globals()[metric](json.dumps(user_data), json.dumps(job_details))

                    if metric == "overlap_coefficient":
                        title = "Token Space"
                        help_text = "Token space compares texts by looking at the exact token (words part of a word) they use. It's like a word-for-word matching game. This method is great for spotting specific terms or skills, making it especially useful for technical resumes. However, it might miss similarities when different words are used to express the same idea. For example, \"manage\" and \"supervise\" would be seen as different in token space, even though they often mean the same thing in job descriptions."
                    elif metric == "cosine_similarity":
                        title = "Latent Space"
                        help_text = "Latent space looks at the meaning behind the words, not just the words themselves. It's like comparing the overall flavor of dishes rather than their ingredient lists. In this space, words with similar meanings are grouped together, even if they're spelled differently. For example, \"innovate\" and \"create\" would be close in latent space because they convey similar ideas. This method is particularly good at understanding context and themes, which is how AI language models actually process text. It's done by calculating cosine similarity between vector embeddings of two texts. By using latent space, we can see if the AI-generated resume captures the essence of the job description, even if it uses different wording."

                    st.caption(f"## **:rainbow[{title}]**", help=help_text)
                    col_m_1, col_m_2, col_m_3 = st.columns(3)
                    col_m_1.metric(label=":green[User Personalization Score]", value=f"{user_personalization:.3f}", delta="(new resume, old resume)", delta_color="off")
                    col_m_2.metric(label=":blue[Job Alignment Score]", value=f"{job_alignment:.3f}", delta="(new resume, job details)", delta_color="off")
                    col_m_3.metric(label=":violet[Job Match Score]", value=f"{job_match:.3f}", delta="[old resume, job details]", delta_color="off")
                st.markdown("---")

            # Build Cover Letter
            if get_cover_letter_button:
                with st.status("Building cover letter..."):
                    cv_details, cv_path = resume_llm.cover_letter_generator(job_details, user_data, is_st=True)
                cv_col_1, cv_col_2 = st.columns([0.7, 0.3])
                with cv_col_1:
                    st.subheader("Generated Cover Letter")
                with cv_col_2:
                    cv_data = read_file(cv_path, "rb")
                    st.download_button(label="Download CV ⬇",
                                    data=cv_data,
                                    file_name=os.path.basename(cv_path),
                                    # on_click=download_pdf(cv_path),
                                    key="download_cv_button",
                                    mime="application/pdf", 
                                    use_container_width=True)
                st.markdown(cv_details, unsafe_allow_html=True)
                st.markdown("---")
                st.toast("cover letter generated successfully!", icon="✅")
            
            st.toast(f"Done", icon="👍🏻")
            st.success(f"Done", icon="👍🏻")
            st.balloons()
            
            refresh = st.button("Refresh")

            if refresh:
                st.caching.clear_cache()
                st.rerun()
        
except Exception as e:
    st.error(f"An error occurred: {e}")
    st.markdown("<h3 style='text-align: center;'>Please try again! Check the log in the dropdown for more details.</h3>", unsafe_allow_html=True)
    st.stop()

st.link_button("Report Feedback, Issues, or Contribute!", "https://github.com/Ztrimus/job-llm/issues", use_container_width=True)