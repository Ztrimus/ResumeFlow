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
from openai import OpenAI
import google.generativeai as genai
from zlm.utils.utils import parse_json_markdown
import pandas as pd

class ChatGPT:
    def __init__(self, api_key, system_prompt):
        self.system_prompt = {"role": "system", "content": system_prompt}
        self.client = OpenAI(api_key=api_key)
    
    def get_response(self, prompt, expecting_longer_output=False, need_json_output=False):
        user_prompt = {"role": "user", "content": prompt}

        try:
            # TODO: Decide value(temperature, top_p, max_tokens, stop) to get apt response
            completion = self.client.chat.completions.create(
                model="gpt-4-1106-preview",
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
    
    def get_embedding(self, text, model="text-embedding-ada-002"):
        try:
            text = text.replace("\n", " ")
            return self.client.embeddings.create(input = [text], model=model).data[0].embedding
        except Exception as e:
            print(e)

class Gemini:
    # TODO: Test and Improve support for Gemini API
    def __init__(self, api_key, system_prompt):
        genai.configure(api_key=api_key)
        self.system_prompt = "System Prompt\n======\n" + system_prompt
    
    def get_response(self, prompt, expecting_longer_output=False, need_json_output=False):
        try:
            user_prompt = "\n\nUser Prompt\n======\n" + prompt
            entire_prompt = self.system_prompt + user_prompt
            
            model = genai.GenerativeModel('gemini-pro')
            content = model.generate_content(
                entire_prompt,
                generation_config={
                    "temperature": 0.3, 
                    "max_output_tokens": 4000 if expecting_longer_output else None,
                    "top_k": 4
                    }
                )
            
            if need_json_output:
                return parse_json_markdown(content.text)
            else:
                return content.text
        
        except Exception as e:
            print(e)
            return None
    
    def get_embedding(self, content, model="models/embedding-001", task_type="retrieval_document"):
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


class TogetherAI:
    def __init__(self, api_key, system_prompt):
        self.system_prompt = {"role": "system", "content": system_prompt}
        self.client = OpenAI(
            api_key=api_key,
            base_url='https://api.together.xyz',
        )
    
    def get_response(self, prompt, expecting_longer_output=False, need_json_output=False):
        user_prompt = {"role": "user", "content": prompt}

        try:
            if expecting_longer_output:
                completion = self.client.chat.completions.create(
                    model="mistralai/Mistral-7B-Instruct-v0.2",
                    messages = [self.system_prompt, user_prompt],
                    max_tokens = 7000,
                )
            else:
                completion = self.client.chat.completions.create(
                    model="mistralai/Mistral-7B-Instruct-v0.2",
                    messages = [self.system_prompt, user_prompt],
                )

            response = completion.choices[0].message
            content = response.content.strip()

            if need_json_output:
                return parse_json_markdown(content)
            else:
                return content
        
        except Exception as e:
            print(e)

class Llama2:
    def __init__(self, hf_token, system_prompt):
        # !pip install sentencepiece==0.1.99
        # !pip install transformers==4.31.0
        # !pip install accelerate==0.21.0
        # !pip install bitsandbytes==0.41.1
        # https://github.com/facebookresearch/llama/blob/main/llama/generation.py#L212
        
        from transformers import LlamaForCausalLM, LlamaTokenizer

        self.system_prompt = system_prompt
        self.tokenizer = LlamaTokenizer.from_pretrained("meta-llama/Llama-2-7b-chat-hf", token=hf_token)
        self.model = LlamaForCausalLM.from_pretrained("meta-llama/Llama-2-7b-chat-hf", load_in_8bit=True, device_map="auto", token=hf_access_token)
        self.generation_kwargs = {
            "max_new_tokens": 512,
            "top_p": 0.9,
            "temperature": 0.6,
            "repetition_penalty": 1.2,
            "do_sample": True,
        }

    def get_response(self, prompt_text, need_json_output=False):
        B_INST, E_INST = "[INST]", "[/INST]"
        B_SYS, E_SYS = "<<SYS>>\n", "\n<</SYS>>\n\n"

        # Special format required by the Llama2 Chat Model where we can use system messages to provide more context about the task
        prompt = f"{B_INST} {B_SYS} {self.system_prompt} {E_SYS} {prompt_text} {E_INST}"

        prompt_ids = tokenizer(prompt, return_tensors="pt")
        prompt_size = prompt_ids['input_ids'].size()[1]

        generate_ids = model.generate(prompt_ids.input_ids.to(model.device), **self.generation_kwargs)
        generate_ids = generate_ids.squeeze()

        response = tokenizer.decode(generate_ids.squeeze()[prompt_size+1:], skip_special_tokens=True).strip()

        if need_json_output:
                return parse_json_markdown(response)
        else:
            return response

        return response

# TODO: https://ai.google.dev/tutorials/python_quickstart#use_embeddings
def compute_embedding(self, chunks):
    try:
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        vector_embedding = FAISS.from_texts( texts = chunks, embedding=embeddings)
        return vector_embedding
    except Exception as e:
        print(e)
        return None

# Define a function to compute embeddings for the text   
# def compute_embedding(self, text):
#     response = openai.Embed(
#         input=text,
#         model="text-davinci-003-001",
#         max_tokens=50
#     )
#     return response['embedding']