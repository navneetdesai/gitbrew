import base64

import cohere

from gitbrew.prompts.generate_readme_prompt import GenerateReadmePrompt
from gitbrew.prompts.summarize_file import SummarizeFilePrompt


class Cohere:
    model = "command"
    temperature = 0.9

    def __init__(
        self,
        model=model,
        temperature=temperature,
    ):
        self.model = model
        self.temperature = temperature
        self.client = cohere.Client("uUbn47dYGX2yykHilsz6P79J0TWB7Eupv2QbUnCX")

    def generate_readme(self, summary):
        message = (GenerateReadmePrompt.user_prompt.format(summary=summary),)
        response = self.client.chat(
            message=message[0],
            temperature=0.8,
        )
        answer = response.text

        print(answer)
