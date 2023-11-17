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
import openai

class ChatGPT:
    def __init__(self, openai_api_key, system_prompt):
        self.system_prompt = {"role": "system", "content": system_prompt}
        openai.api_key = openai_api_key
    
    def get_response(self, prompt):
        user_prompt = {"role": "user", "content": prompt}

        try:
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages = [self.system_prompt, user_prompt]
            )   

            response = completion.choices[0].message
            content = response["content"].strip()
            content_json = json.loads(content)
            
            return content_json
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

    def get_response(self, prompt_text):
        B_INST, E_INST = "[INST]", "[/INST]"
        B_SYS, E_SYS = "<<SYS>>\n", "\n<</SYS>>\n\n"

        # Special format required by the Llama2 Chat Model where we can use system messages to provide more context about the task
        prompt = f"{B_INST} {B_SYS} {self.system_prompt} {E_SYS} {prompt_text} {E_INST}"

        prompt_ids = tokenizer(prompt, return_tensors="pt")
        prompt_size = prompt_ids['input_ids'].size()[1]

        generate_ids = model.generate(prompt_ids.input_ids.to(model.device), **self.generation_kwargs)
        generate_ids = generate_ids.squeeze()

        response = tokenizer.decode(generate_ids.squeeze()[prompt_size+1:], skip_special_tokens=True).strip()

        return response