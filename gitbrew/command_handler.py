"""
Handler for git commands
"""
import os
import re
import subprocess

from dotenv import load_dotenv
from llms.openai import OpenAI
from PyInquirer import prompt
from rich.console import Console

from gitbrew.prompts.generate_command_prompt import GenerateCommandPrompt

from .constants import SafeCommands
from .exceptions import InvalidAnswerFormatException
from .questions import Questions


class CommandHandler:
    def __init__(self, model="gpt-3.5-turbo", temperature=0.2, debug=False):
        load_dotenv()
        openai_api_key = os.getenv("OPENAI_API_KEY")
        self.console = Console()
        self.debug = debug
        self.openai_client = OpenAI(
            openai_api_key, model=model, temperature=temperature
        )
        self.START_TAG = "<START>"
        self.END_TAG = "<END>"
        self.SEP_TAG = "<SEP>"
        self.COMMAND_PATTERN = re.compile(r"<START>(.*?)<END>", re.DOTALL)
        self.CLARIFICATION_PATTERN = re.compile(r"<CLARIFY>(.*?)</CLARIFY", re.DOTALL)

    def handle(self, line):
        """
        Executes commands with confirmation and safety
        Generates the prompt, retrieves answer from the model,
        extracts commands from it and executes them
        """
        answer = self.ask_llm(line)
        # answer = """<CLARIFY>
        # Are you asking for the URL or name of the remote repository in your git project?
        # </CLARIFY>"""
        self.debug and self.console.log(f"LLM's answer: {answer}")
        commands = self.extract_commands(answer) or self._get_clarification(
            answer, GenerateCommandPrompt.prompt.format(user_intention=line)
        )
        self._execute_commands(commands)

    def ask_llm(self, line):
        _prompt = GenerateCommandPrompt.prompt.format(user_intention=line)
        _prompt = [{"role": "user", "content": _prompt}]
        return self.openai_client.ask_llm(_prompt)

    def extract_commands(self, answer):
        """
        Extract commands from the answer
        If clarification present, return [] otherwise return list of commands
        Update command history
        :param answer:
        :return: list of commands in the answer
        """
        # Todo: Filter commands separated by <SEP> tag
        if commands := re.search(self.COMMAND_PATTERN, answer):
            extracted_commands = list(
                map(lambda s: s.strip(), commands[1].split(self.SEP_TAG))
            )
            return [] if "<CLARIFY>" in answer else extracted_commands
        if "<CLARIFY>" in answer:
            return []
        raise InvalidAnswerFormatException("Answer does not contain commands")

    def _execute_commands(self, commands):
        """
        Execute commands after confirmation from the user

        For each command, checks if its whitelisted (safe / read-only), and executes it.
        If it's not safe, ask for confirmation from the user

        """
        for command in commands:
            command_list = command.split()
            # print(command)
            # Todo : subcommand is --super-prefix=path
            if (
                command_list[1] not in SafeCommands.commands
                and self.get_user_confirmation(command)
                or command_list[1] in SafeCommands.commands
            ):
                print(f"Executing: {command}")
                # Todo : Add error handling here
                result = subprocess.check_output(
                    command_list, cwd=".", universal_newlines=True
                )
                print(result)
                # Todo: check for <branch_name> etc in the command

            else:
                print("Aborting...")
                return

    @staticmethod
    def get_user_confirmation(command):
        """
        Gets user confirmation for the command
        :param command: To be executed on confirmation
        :return: True if user choose yes, no otherwise
        """
        # print(command)
        prompt_string = Questions.USER_CONFIRMATION
        prompt_string[0][
            "message"
        ] = "We will run `{command}` Are you sure you want to proceed?".format(
            command=command
        )
        answer = prompt(prompt_string)["confirmation"]
        return answer == "Yes"

    def _get_clarification(self, answer, line):
        """
        Ask the user for clarification
        :param answer:
        :param line:
        :return:
        """
        clarification = re.search(self.CLARIFICATION_PATTERN, answer)

        question = [
            {
                "type": "input",
                "name": "clarification",
                "message": clarification[1],
            }
        ]

        answer = prompt(question)["clarification"]
        conversation = f"{line}\n{clarification[1]}:{answer}"
        line = f"This is our conversation: `{conversation}`. Based on the clarification provided, generate the git commands."
        answer = self.ask_llm(line=line)

        if commands := self.extract_commands(answer):
            return commands
        else:
            return self._get_clarification(answer, conversation)
