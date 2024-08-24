'''
-----------------------------------------------------------------------
File: LLM.py
Creation Time: Nov 1st 2023 1:40 am
Author: Saurabh Zinjad
Developer Email: zinjadsaurabh1997@gmail.com
Copyright (c) 2023 Saurabh Zinjad. All rights reserved | GitHub: Ztrimus
-----------------------------------------------------------------------
'''
import json
import textwrap
import pandas as pd
import streamlit as st
from openai import OpenAI
from langchain_community.llms.ollama import Ollama
from langchain_ollama import OllamaEmbeddings
import google.generativeai as genai
from google.generativeai.types.generation_types import GenerationConfig

from zlm.utils.utils import parse_json_markdown
from zlm.variables import GEMINI_EMBEDDING_MODEL, GPT_EMBEDDING_MODEL, OLLAMA_EMBEDDING_MODEL

class ChatGPT:
    def __init__(self, api_key, model, system_prompt):
        if system_prompt.strip():
            self.system_prompt = {"role": "system", "content": system_prompt}
        self.client = OpenAI(api_key=api_key)
        self.model = model
    
    def get_response(self, prompt, expecting_longer_output=False, need_json_output=False):
        user_prompt = {"role": "user", "content": prompt}

        try:
            # TODO: Decide value(temperature, top_p, max_tokens, stop) to get apt response
            completion = self.client.chat.completions.create(
                model=self.model,
                messages = [self.system_prompt, user_prompt],
                temperature=0,
                max_tokens = 4000 if expecting_longer_output else None,
                response_format = { "type": "json_object" } if need_json_output else None
            )

            response = completion.choices[0].message
            content = response.content.strip()
            
            if need_json_output:
                return parse_json_markdown(content)
            else:
                return content
        
        except Exception as e:
            print(e)
            st.error(f"Error in OpenAI API, {e}")
            st.markdown("<h3 style='text-align: center;'>Please try again! Check the log in the dropdown for more details.</h3>", unsafe_allow_html=True)
    
    def get_embedding(self, text, model=GPT_EMBEDDING_MODEL, task_type="retrieval_document"):
        try:
            text = text.replace("\n", " ")
            return self.client.embeddings.create(input = [text], model=model).data[0].embedding
        except Exception as e:
            print(e)

class Gemini:
    # TODO: Test and Improve support for Gemini API
    def __init__(self, api_key, model, system_prompt):
        genai.configure(api_key=api_key)
        self.system_prompt = system_prompt
        self.model = model
    
    def get_response(self, prompt, expecting_longer_output=False, need_json_output=False):
        try:
            model = genai.GenerativeModel(
                model_name=self.model,
                system_instruction=self.system_prompt
                )
            
            content = model.generate_content(
                contents=prompt,
                generation_config=GenerationConfig(
                    temperature=0.7,
                    max_output_tokens = 4000 if expecting_longer_output else None,
                    response_mime_type = "application/json" if need_json_output else None
                    )
                )

            if need_json_output:
                result = parse_json_markdown(content.text)
            else:
                result = content.text
            
            if result is None:
                st.write("LLM Response")
                st.markdown(f"```json\n{content.text}\n```")

            return result
        
        except Exception as e:
            print(e)
            st.error(f"Error in Gemini API, {e}")
            st.markdown("<h3 style='text-align: center;'>Please try again! Check the log in the dropdown for more details.</h3>", unsafe_allow_html=True)
            return None
    
    def get_embedding(self, content, model=GEMINI_EMBEDDING_MODEL, task_type="retrieval_document"):
        try:
            def embed_fn(data):
                result = genai.embed_content(
                    model=model,
                    content=data,
                    task_type=task_type,
                    title="Embedding of json text" if task_type in ["retrieval_document", "document"] else None)
                
                return result['embedding']
            
            df = pd.DataFrame(content)
            df.columns = ['chunk']
            df['embedding'] = df.apply(lambda row: embed_fn(row['chunk']), axis=1)
            
            return df
        
        except Exception as e:
            print(e)

class OllamaModel:
    def __init__(self, model, system_prompt):
        self.model = model
        self.system_prompt = system_prompt
    
    def get_response(self, prompt, expecting_longer_output=False, need_json_output=False):
        try:
            llm = Ollama(
                model=self.model, 
                system=self.system_prompt,
                temperature=0.8, 
                top_p=0.999, 
                top_k=250,
                num_predict=4000 if expecting_longer_output else None,
                # format='json' if need_json_output else None,
                )
            content = llm.invoke(prompt)

            if need_json_output:
                result = parse_json_markdown(content)
            else:
                result = content
            
            if result is None:
                st.write("LLM Response")
                st.markdown(f"```json\n{content.text}\n```")

            return result
        
        except Exception as e:
            print(e)
            st.error(f"Error in Ollama model - {self.model}, {e}")
            st.markdown("<h3 style='text-align: center;'>Please try again! Check the log in the dropdown for more details.</h3>", unsafe_allow_html=True)
            return None
    
    def get_embedding(self, content, model=OLLAMA_EMBEDDING_MODEL, task_type="retrieval_document"):
        try:
            def embed_fn(data):
                embedding = OllamaEmbeddings(model=model)
                result = embedding.embed_query(data)
                return result
            
            df = pd.DataFrame(content)
            df.columns = ['chunk']
            df['embedding'] = df.apply(lambda row: embed_fn(row['chunk']), axis=1)
            
            return df
        
        except Exception as e:
            print(e)