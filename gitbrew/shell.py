import cmd
import os
import subprocess
import sys
from typing import Any

import openai
from dotenv import load_dotenv
from gitpy import GitPy
from PyInquirer import prompt
from questions import Questions
from rich.console import Console
from sklearn.metrics.pairwise import cosine_similarity

from gitbrew.command_handler import CommandHandler
from gitbrew.generate_readme import ReadmeGenerator
from gitbrew.issue_manager import IssueManager
from gitbrew.llms import OpenAI
from gitbrew.pull_requests import PullRequestReviewer


class Shell(cmd.Cmd):
    prompt = "gitbrew> "
    exit_keywords = ["exit", "quit"]
    CHOICES = {"All issues": "all", "Open issues": "open", "Closed issues": "closed"}
    MESSAGE = "Welcome to gitbrew! Enter `quit` or `exit` to exit the application.\n"

    def __init__(self, debug=False):
        super().__init__()
        load_dotenv()
        self.openai_agent = OpenAI(os.getenv("OPENAI_API_KEY"), temperature=0.35)
        self.DEBUG = debug
        self.git_helper = GitPy(os.getenv("GITHUB_TOKEN"))
        self.embeddings_cache = {}  # local cache
        self.command_handler = CommandHandler(debug=self.DEBUG)  # git command handler
        self.pull_request_reviewer = (
            PullRequestReviewer()
        )  # pull request reviewer handler
        self.readme_generator = ReadmeGenerator()  # readme generator handler
        self.issue_manager = IssueManager()  # issue manager handler
        self.console = Console()
        self.UTILITIES = {
            "Generate a Readme": self._readme_generation_handler,
            "Work with github issues": self._issue_manager_handler,
            "Work with git": self._git_command_handler,
            "Review a pull request": self._pull_request_handler,
            "Exit": self.do_exit,
        }

    @staticmethod
    def do_exit(arg):
        """
        Handler for "exit" keyword
        :param arg: Optional args
        :return: True
        """
        return True

    @staticmethod
    def do_quit(arg):
        """
        Handler for "quit" keyword
        :param arg: Optional args
        :return: True
        """
        return True

    def cmdloop(self, intro=None):
        """
        Create a command line loop
        :param intro: Intro
        :return: None
        """
        if intro:
            self.intro = intro
        try:
            super().cmdloop()
        except KeyboardInterrupt:
            print("\nExiting...")
            sys.exit(0)

    def do_help(self, arg: str):
        """
        Handler for "help" keyword
        :param arg: Optional args
        :return: True
        """
        # fetch all methods that start with "do_"
        # Todo: to be implemented
        pass

    def default(self, line: str) -> None:
        """
        Handler for unknown commands / methods
        :param line: text input from cmd
        :return:
        """
        self._git_command_handler(line)

    def preloop(self) -> None:
        self._choose_utility()

    def _choose_utility(self, line=None):
        """
        Choose utility based on user input
        Create embedding from user input and choose module with
        the closest match

        :param line:
        :return:
        """
        if line:
            print(f"I don't understand what you mean by: {line}")
        questions = Questions.CHOOSE_UTILITY
        self.UTILITIES.get(prompt(questions)["utility"])()

    def _pull_request_handler(self):
        """
        Handler for pull requests
        :return:
        """
        self.DEBUG and print("Called pull request handler")
        self.pull_request_reviewer.handle()

    def _readme_generation_handler(self):
        """
        Handler for readme generation
        :return:
        """
        self.DEBUG and print("Generating readme")
        self.readme_generator.handle()

    def _git_command_handler(self, line):
        print("Called git command handler")

    def _issue_manager_handler(self):
        self.DEBUG and print("Called issue manager handler")
        self.issue_manager.handle()
