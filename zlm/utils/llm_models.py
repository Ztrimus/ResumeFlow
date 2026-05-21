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
import logging
import textwrap
from typing import Type

import instructor
import pandas as pd
import streamlit as st
from openai import OpenAI, RateLimitError, APITimeoutError, InternalServerError, APIConnectionError
from langchain_ollama import OllamaLLM, OllamaEmbeddings
import google.generativeai as genai
from google.generativeai.types.generation_types import GenerationConfig
from google.api_core.exceptions import ResourceExhausted, ServiceUnavailable, DeadlineExceeded
from pydantic import BaseModel
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
    before_sleep_log,
)

from zlm.variables import GEMINI_EMBEDDING_MODEL, GPT_EMBEDDING_MODEL, OLLAMA_EMBEDDING_MODEL

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Shared tenacity retry configs
# ---------------------------------------------------------------------------

_openai_retry = dict(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=30),
    retry=retry_if_exception_type((RateLimitError, APITimeoutError, InternalServerError, APIConnectionError)),
    reraise=True,
    before_sleep=before_sleep_log(logger, logging.WARNING),
)

_gemini_retry = dict(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=30),
    retry=retry_if_exception_type((ResourceExhausted, ServiceUnavailable, DeadlineExceeded)),
    reraise=True,
    before_sleep=before_sleep_log(logger, logging.WARNING),
)

# Ollama is local; retry on connection / timeout only
try:
    import httpx
    _ollama_retry_exc = (httpx.ConnectError, httpx.TimeoutException)
except ImportError:
    _ollama_retry_exc = (ConnectionError, TimeoutError)

_ollama_retry = dict(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=10),
    retry=retry_if_exception_type(_ollama_retry_exc),
    reraise=True,
    before_sleep=before_sleep_log(logger, logging.WARNING),
)


# ---------------------------------------------------------------------------
# ChatGPT
# ---------------------------------------------------------------------------

class ChatGPT:
    def __init__(self, api_key, model, system_prompt):
        self.model = model
        self.system_prompt = system_prompt.strip()
        raw_client = OpenAI(api_key=api_key)
        self.client = instructor.from_openai(raw_client)

    @retry(**_openai_retry)
    def get_response(
        self,
        prompt: str,
        expecting_longer_output: bool = False,
        response_model: Type[BaseModel] | None = None,
    ):
        """Call the OpenAI API.

        Args:
            prompt: User prompt text.
            expecting_longer_output: Raise max_tokens to 4000 when True.
            response_model: Pydantic model class for structured output.
                When provided, Instructor guarantees a validated instance is
                returned (auto-retries up to 3× on validation failure).
                When None, returns the raw text string.
        """
        messages = []
        if self.system_prompt:
            messages.append({"role": "system", "content": self.system_prompt})
        messages.append({"role": "user", "content": prompt})

        extra = {}
        if expecting_longer_output:
            extra["max_tokens"] = 4000

        try:
            if response_model is not None:
                return self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=0,
                    response_model=response_model,
                    max_retries=3,
                    **extra,
                )
            else:
                # Plain-text path (e.g. cover letter)
                completion = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=0,
                    response_model=None,
                    **extra,
                )
                return completion.choices[0].message.content.strip()

        except Exception as e:
            logger.error("OpenAI API error: %s", e)
            st.error(f"Error in OpenAI API: {e}")
            st.markdown(
                "<h3 style='text-align: center;'>Please try again! "
                "Check the log in the dropdown for more details.</h3>",
                unsafe_allow_html=True,
            )
            return None

    def get_embedding(self, text, model=GPT_EMBEDDING_MODEL, task_type="retrieval_document"):
        try:
            text = text.replace("\n", " ")
            return self.client.embeddings.create(input=[text], model=model).data[0].embedding
        except Exception as e:
            logger.error("OpenAI embedding error: %s", e)


# ---------------------------------------------------------------------------
# Gemini
# ---------------------------------------------------------------------------

class Gemini:
    def __init__(self, api_key, model, system_prompt):
        genai.configure(api_key=api_key)
        self.system_prompt = system_prompt
        self.model = model

    def _make_instructor_client(self):
        """Build a fresh Instructor-patched Gemini client."""
        genai_model = genai.GenerativeModel(
            model_name=self.model,
            system_instruction=self.system_prompt,
        )
        return instructor.from_gemini(client=genai_model, mode=instructor.Mode.GEMINI_JSON)

    @retry(**_gemini_retry)
    def get_response(
        self,
        prompt: str,
        expecting_longer_output: bool = False,
        response_model: Type[BaseModel] | None = None,
    ):
        """Call the Gemini API.

        Args:
            prompt: User prompt text.
            expecting_longer_output: Raise max_output_tokens to 4000 when True.
            response_model: Pydantic model class for structured output.
                When provided, Instructor guarantees a validated instance is
                returned (auto-retries up to 3× on validation failure).
                When None, returns the raw text string.
        """
        try:
            if response_model is not None:
                client = self._make_instructor_client()
                extra = {}
                if expecting_longer_output:
                    extra["max_tokens"] = 4000
                return client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    response_model=response_model,
                    max_retries=3,
                    **extra,
                )
            else:
                # Plain-text path (e.g. cover letter)
                model = genai.GenerativeModel(
                    model_name=self.model,
                    system_instruction=self.system_prompt,
                )
                content = model.generate_content(
                    contents=prompt,
                    generation_config=GenerationConfig(
                        temperature=0.7,
                        max_output_tokens=4000 if expecting_longer_output else None,
                    ),
                )
                return content.text

        except Exception as e:
            logger.error("Gemini API error: %s", e)
            st.error(f"Error in Gemini API: {e}")
            st.markdown(
                "<h3 style='text-align: center;'>Please try again! "
                "Check the log in the dropdown for more details.</h3>",
                unsafe_allow_html=True,
            )
            return None

    def get_embedding(self, content, model=GEMINI_EMBEDDING_MODEL, task_type="retrieval_document"):
        try:
            def embed_fn(data):
                result = genai.embed_content(
                    model=model,
                    content=data,
                    task_type=task_type,
                    title="Embedding of json text" if task_type in ["retrieval_document", "document"] else None,
                )
                return result["embedding"]

            df = pd.DataFrame(content)
            df.columns = ["chunk"]
            df["embedding"] = df.apply(lambda row: embed_fn(row["chunk"]), axis=1)
            return df

        except Exception as e:
            logger.error("Gemini embedding error: %s", e)


# ---------------------------------------------------------------------------
# OllamaModel
# ---------------------------------------------------------------------------

class OllamaModel:
    def __init__(self, model, system_prompt):
        self.model = model
        self.system_prompt = system_prompt

    @retry(**_ollama_retry)
    def get_response(
        self,
        prompt: str,
        expecting_longer_output: bool = False,
        response_model: Type[BaseModel] | None = None,
    ):
        """Call a local Ollama model.

        Args:
            prompt: User prompt text.
            expecting_longer_output: Raise num_predict to 4000 when True.
            response_model: Pydantic model class for structured output.
                When provided, Ollama is asked for JSON and the response is
                validated against the schema. When None, returns raw text.

        Note:
            Ollama does not support Instructor's validation-retry loop natively.
            JSON mode is enabled via ``format='json'``; if parsing fails the
            raw response is logged and None is returned.
        """
        try:
            llm = OllamaLLM(
                model=self.model,
                system=self.system_prompt,
                temperature=0.8,
                top_p=0.999,
                top_k=250,
                num_predict=4000 if expecting_longer_output else None,
                format="json" if response_model is not None else None,
            )
            content = llm.invoke(prompt)

            if response_model is not None:
                try:
                    parsed = json.loads(content)
                    return response_model.model_validate(parsed)
                except (json.JSONDecodeError, Exception) as parse_err:
                    logger.error("Ollama JSON parse/validation error: %s\nRaw response: %s", parse_err, content)
                    st.write("LLM Response (parse failed)")
                    st.markdown(f"```json\n{content}\n```")
                    return None

            return content

        except Exception as e:
            logger.error("Ollama model error (%s): %s", self.model, e)
            st.error(f"Error in Ollama model - {self.model}: {e}")
            st.markdown(
                "<h3 style='text-align: center;'>Please try again! "
                "Check the log in the dropdown for more details.</h3>",
                unsafe_allow_html=True,
            )
            return None

    def get_embedding(self, content, model=OLLAMA_EMBEDDING_MODEL, task_type="retrieval_document"):
        try:
            def embed_fn(data):
                embedding = OllamaEmbeddings(model=model)
                return embedding.embed_query(data)

            df = pd.DataFrame(content)
            df.columns = ["chunk"]
            df["embedding"] = df.apply(lambda row: embed_fn(row["chunk"]), axis=1)
            return df

        except Exception as e:
            logger.error("Ollama embedding error: %s", e)
