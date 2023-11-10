"""
Handler for git commands
"""
import os
import re

import openai
from dotenv import load_dotenv

from gitbrew.prompts.generate_command_prompt import GenerateCommandPrompt

from .exceptions import InvalidAnswerFormatException


class CommandHandler:
    def __init__(self):
        load_dotenv()
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.model = "gpt-3.5-turbo"
        self.temperature = 0.2
        self.START_TAG = "<START>"
        self.END_TAG = "<END>"
        self.SEP_TAG = "<SEP>"
        self.COMMAND_PATTERN = re.compile(r"<START>(.*?)<END>", re.DOTALL)

    def handle(self, line):
        # prompt = GenerateCommandPrompt.prompt.format(user_intention=line)
        # response = openai.ChatCompletion.create(
        #     model=self.model,
        #     messages=[{"role": "user", "content": prompt}],
        #     temperature=self.temperature,
        # )
        # answer = response.choices[0]["message"]["content"].strip()
        # print(f'Answer: {answer}')
        answer = """
        <START>
git add .
<SEP>
git commit -m "Add all changes to remote repository"
<SEP>
git push origin
<END>
        """
        commands = self.extract_commands(answer)
        print(commands)

    def extract_commands(self, answer):
        """
        Extract commands from the answer
        :param answer:
        :return: list of commands in the answer
        """
        if commands := re.search(self.COMMAND_PATTERN, answer)[1]:
            return list(map(lambda s: s.strip(), commands.split(self.SEP_TAG)))
        else:
            raise InvalidAnswerFormatException("Answer does not contain commands")
