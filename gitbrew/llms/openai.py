"""
Wrappers for the OpenAI API
"""
import base64

import openai

from gitbrew.prompts.generate_readme_prompt import GenerateReadmePrompt
from gitbrew.prompts.summarize_file import SummarizeFilePrompt


class OpenAI:
    engine = "gpt-3.5-turbo"
    max_tokens = 4096
    temperature = 0.2
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
        openai.api_key = api_key
        self.engine = engine
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
            response = openai.ChatCompletion.create(
                model=self.engine,
                messages=[{"role": "user", "content": prompt}],
                temperature=self.temperature,
            )
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
        response = openai.ChatCompletion.create(
            model=self.engine,
            messages=messages,
            temperature=self.temperature,
        )
        return response.choices[0]["message"]["content"].strip()
