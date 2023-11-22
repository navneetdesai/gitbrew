"""
Wrappers for the OpenAI API
"""

import os

import openai


class OpenAI:
    # set defaults
    chat_model = "gpt-3.5-turbo"
    embeddings_model = "text-embedding-ada-002"
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
        """
        Wrapper for the OpenAI API
        :param api_key:
        :param chat_model:
        :param embeddings_model:
        :param max_tokens:
        :param temperature:
        :param top_p:
        :param frequency_penalty:
        :param presence_penalty:
        """
        openai.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.chat_model = chat_model
        self.embeddings_model = embeddings_model
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.top_p = top_p
        self.frequency_penalty = frequency_penalty
        self.presence_penalty = presence_penalty

    def ask_llm(self, prompt):
        """
        Uses the openai ChatCompletion API to generate a response
        :param prompt:
        :return:
        """
        try:
            response = openai.ChatCompletion.create(
                model=self.chat_model,
                messages=prompt,
                temperature=self.temperature,
            )
        except openai.error.OpenAIError as e:
            print("Error: ", e)
            return

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

    @staticmethod
    def create_message(system_prompt=None, user_prompt=None):
        """
        Generate a message for the LLM with given prompts
        for the chat completion API
        :param user_prompt: User prompt
        :param system_prompt: System prompt (Optional)
        :return:
        """
        system_message = {"role": "system", "content": system_prompt}
        user_message = {"role": "user", "content": user_prompt}
        if not user_prompt:
            raise ValueError("User prompt cannot be empty")
        return [system_message, user_message] if system_prompt else [user_message]
