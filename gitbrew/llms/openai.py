"""
Wrappers for the OpenAI API
"""
import base64
import os

import openai

from gitbrew.prompts.generate_readme_prompt import GenerateReadmePrompt
from gitbrew.prompts.summarize_file import SummarizeFilePrompt


class OpenAI:
    # set defaults
    chat_model = "gpt-3.5-turbo"
    embeddings_model = "text-embedding-ada-002"
    # engine = "gpt-4"
    max_tokens = 4096
    temperature = 0.2
    top_p = 1
    frequency_penalty = 0.25
    presence_penalty = 0.25

    def __init__(
        self,
        api_key,
        chat_model=chat_model,
        embeddings_model=embeddings_model,
        max_tokens=max_tokens,
        temperature=temperature,
        top_p=top_p,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
    ):
        openai.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.chat_model = chat_model
        self.embeddings_model = embeddings_model
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.top_p = top_p
        self.frequency_penalty = frequency_penalty
        self.presence_penalty = presence_penalty

    def summarize_file(self, files):
        result = []
        for file in files:
            content = base64.b64decode(file.content).decode("utf-8")[:3000]
            prompt = SummarizeFilePrompt.template.format(
                filename=file.name, content=content
            )
            messages = [
                {"role": "system", "content": GenerateReadmePrompt.system_prompt},
                {
                    "role": "user",
                    "content": prompt,
                },
            ]
            response = self.ask_llm(messages)
            # Todo: remove after testing
            # response = openai.ChatCompletion.create(
            #     model=self.model,
            #     messages=[{"role": "user", "content": prompt}],
            #     temperature=self.temperature,
            # )
            result.append(response.choices[0]["message"]["content"].strip())
        return result

    def generate_readme(self, summary):
        messages = [
            {"role": "system", "content": GenerateReadmePrompt.system_prompt},
            {
                "role": "user",
                "content": GenerateReadmePrompt.user_prompt.format(summary=summary),
            },
        ]
        print("Making an API call to OpenAI for generating readme")
        return self.ask_llm(messages)
        # Todo: Remove after readme is tested again
        # response = openai.ChatCompletion.create(
        #     model=self.model,
        #     messages=messages,
        #     temperature=self.temperature,
        # )
        # return response.choices[0]["message"]["content"].strip()

    def ask_llm(self, prompt):
        """
        Uses the openai ChatCompletion API to generate a response
        :param prompt:
        :return:
        """
        response = openai.ChatCompletion.create(
            model=self.chat_model,
            messages=prompt,
            temperature=self.temperature,
        )
        return response.choices[0]["message"]["content"].strip()

    def create_embedding(self, text):
        """
        Uses the openai EmbeddingCreate API to generate an embedding
        :param text:
        :return:
        """
        return openai.Embedding.create(
            input=text,
            model=self.embeddings_model,
        )
