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
from .prompts.explain_command_prompt import ExplainCommandPrompt
from .questions import Questions


class CommandHandler:
    def __init__(self, logger, model="gpt-3.5-turbo", temperature=0.2, debug=False):
        load_dotenv()
        openai_api_key = os.getenv("OPENAI_API_KEY")
        self.console = Console()
        self.DEBUG = debug
        self.openai_client = OpenAI(
            openai_api_key, chat_model=model, temperature=temperature
        )
        self.logger = logger
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
        self.logger.debug(f"LLM: {answer}")
        commands = self.extract_commands(answer) or self._get_clarification(
            answer, GenerateCommandPrompt.template.format(user_intention=line)
        )
        self._execute_commands(commands)

    def ask_llm(self, line):
        _prompt = GenerateCommandPrompt.template.format(user_intention=line)
        _prompt = [{"role": "user", "content": _prompt}]
        self.logger.debug(f"Prompt: {_prompt}")
        return self.openai_client.ask_llm(_prompt)

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
            if not command.startswith("git"):
                self.logger.info(f"Comment: {command}")
        for command in commands:
            command_list = command.split()
            command = self.sanitize_command(
                command
            )  # check for <branch_name> etc in the command
            if command_list[0] != "git":  # check if it's a comment
                pass
            elif (  # check if it's a safe command or get confirmation from the user
                command_list[1] not in SafeCommands.commands
                and self.get_user_confirmation(command)
                or command_list[1] in SafeCommands.commands
            ):
                try:
                    print(f"Executing: {command}")
                    # result = subprocess.check_output(
                    #     command_list,
                    #     cwd=".",
                    #     universal_newlines=True,
                    #     stderr=subprocess.STDOUT,
                    # )
                    # self.logger.debug(f"Result: {result}")
                except subprocess.CalledProcessError as e:
                    self.logger.error(
                        f"Command '{e.cmd}' failed with return code {e.returncode}"
                    )
                    self.logger.error(f"Output:\n{e.output}")
                    break
                except Exception as e:
                    self.logger.error(f"Error: {e}")
                    break
            else:
                self.logger.info("Aborting...")
                return

    def sanitize_command(self, command):
        """
        Sanitize the command by removing placeholders like <branch_name>

        Loops while the command has a placeholder, and asks the user for the value
        :param command:
        :return:
        """
        while place_holder := re.search(r"<(.*?)>", command):
            question = [
                {
                    "type": "input",
                    "name": "answer",
                    "message": f"Enter {place_holder[1]}",
                }
            ]
            answer = prompt(question)["answer"]
            command = command.replace(f"<{place_holder[1]}>", answer)
            self.logger.info(f"Sanitized command: {command}")
        return command

    def get_user_confirmation(self, command):
        """
        Gets user confirmation for the command
        :param command: To be executed on confirmation
        :return: True if user choose yes, no otherwise
        """
        prompt_string = Questions.USER_CONFIRMATION
        answer = "Explain"
        while answer == "Explain":
            prompt_string[0][
                "message"
            ] = "We will run `{command}` Are you sure you want to proceed?".format(
                command=command
            )
            answer = prompt(prompt_string)["confirmation"]
            # handle explanations
            if answer == "Explain":
                self._print_explanation(command)
        return answer == "Yes"

    def _print_explanation(self, command):
        """
        Called when user chooses "explain" in the confirmation prompt
        Should explain the command and return to the confirmation prompt
        :param command:
        :return:
        """

        content = ExplainCommandPrompt.template.format(command=command)
        explanation = self.openai_client.ask_llm(
            prompt=[{"role": "user", "content": content}]
        )
        print(f"Explanation: {explanation}")

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
