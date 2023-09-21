"""
Wrappers for the OpenAI API
"""

import openai


class OpenAI:
    engine = "gpt-3.5-turbo"
    max_tokens = 2500
    temperature = 0
    top_p = 1
    frequency_penalty = 0.25
    presence_penalty = 0.25

    def __init__(
        self,
        api_key,
        engine=engine,
        max_tokens=max_tokens,
        temperature=temperature,
        top_p=top_p,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
    ):
        self.api_key = api_key
        self.engine = engine
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.top_p = top_p
        self.frequency_penalty = frequency_penalty
        self.presence_penalty = presence_penalty
