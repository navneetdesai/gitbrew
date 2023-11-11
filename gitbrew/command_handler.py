"""
Handler for git commands
"""
import os
import re
import subprocess

import openai
from dotenv import load_dotenv

from gitbrew.prompts.generate_command_prompt import GenerateCommandPrompt

from .constants import ReadOnlyCommands
from .exceptions import InvalidAnswerFormatException


class CommandHandler:
    def __init__(self):
        load_dotenv()
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.model = "gpt-4"
        self.temperature = 0.2
        self.START_TAG = "<START>"
        self.END_TAG = "<END>"
        self.SEP_TAG = "<SEP>"
        self.COMMAND_PATTERN = re.compile(r"<START>(.*?)<END>", re.DOTALL)
        self.history = []

    def handle(self, line):
        prompt = GenerateCommandPrompt.prompt.format(user_intention=line)
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=self.temperature,
        )
        answer = response.choices[0]["message"]["content"].strip()
        # print(f'Answer: {answer}')

        commands = self.extract_commands(answer)
        self._execute_commands(commands)

    def extract_commands(self, answer):
        """
        Extract commands from the answer
        If clarification present, return [] otherwise return list of commands
        Update command history
        :param answer:
        :return: list of commands in the answer
        """
        if commands := re.search(self.COMMAND_PATTERN, answer):
            extracted_commands = list(
                map(lambda s: s.strip(), commands[1].split(self.SEP_TAG))
            )
            self.history.append(extracted_commands)
            return [] if "<CLARIFY>" in answer else extracted_commands
        raise InvalidAnswerFormatException("Answer does not contain commands")

    def _execute_commands(self, commands):
        """
        Execute commands after confirmation from the user
        :param commands:
        :return:
        """
        for command in commands:
            tokens = command.split()
            if tokens[1] in ReadOnlyCommands.commands:
                print(f"Executing command: {command}")
            else:
                user_answer = input(
                    f"Executing `{command}` might change something. Are you sure? (y/n)"
                )
                if user_answer == "y":
                    print(f"Executing command: {command}")
                else:
                    print("Aborting...")
                    return
