import cmd
import os
import subprocess
import sys

from dotenv import load_dotenv
from gitpy import GitPy
from PyInquirer import prompt
from questions import Questions


class Shell(cmd.Cmd):
    prompt = "gitbrew> "
    exit_keywords = ["exit", "quit"]
    CHOICES = {"All issues": "all", "Open issues": "open", "Closed issues": "closed"}

    def do_1(self, arg):
        """
        Testing method for quick routing during unit testing
        :return:
        """
        self.do_issue_interaction()

    def __init__(self):
        super().__init__()
        load_dotenv()
        self.git_helper = GitPy(os.getenv("GITHUB_TOKEN"))

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

    def do_help(self, arg: str):
        """
        Handler for "help" keyword
        :param arg: Optional args
        :return: True
        """
        # fetch all methods that start with "do_"
        print("What would you like to do?")
        for command in self.get_names():
            if command.startswith("do_"):
                print(f" - {command[3:].replace('_', ' ')}")

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

    def default(self, line: str) -> None:
        """
        Handler for unknown commands / methods
        :param line: text input from cmd
        :return:
        """
        if f"do_{line.replace(' ', '_')}" in self.get_names():
            exec(f"self.do_{line.replace(' ', '_')}()")
        else:
            raise AttributeError(f"Unknown command: {line}")

    def do_issue_interaction(self):
        """
        Handler for "issue interaction" keyword
        :return: None
        """
        # ask which repo they want to interact with
        # the remote repo or a custom repo
        questions = Questions.REPO_URL_QUESTIONS
        if prompt(questions)["repo_choice"] == "Remote":
            try:
                command = ["git", "remote", "get-url", "origin"]
                result = subprocess.check_output(
                    command, cwd=".", universal_newlines=True
                )
                print(f"Current repo url is: {result}")
                url = result.strip()
                # Todo: Needs to be better designed
                repo = url.split(":")[1].split(".")[0]
                self.git_helper.repo_str = repo
            except subprocess.CalledProcessError as e:
                print(f"Error: {e}")
                sys.exit(1)
        else:
            # url = https://github.com/quora/pyanalyze

            questions = [
                {
                    "type": "input",
                    "name": "repo_url",
                    "message": "Enter the repository url",
                }
            ]
            url = prompt(questions)["repo_url"]
            self.git_helper.repo_str = self.git_helper.extract_repo(url)

        questions = Questions.ISSUE_INTERACTION_QUESTIONS
        answers = prompt(questions)
        choice = answers["choice"]

        if choice == "List Issues":
            self._list_issues()

    def _list_issues(self):
        questions = Questions.ISSUE_STATUS_QUESTIONS
        self.git_helper.list_issues(self.CHOICES.get(prompt(questions)["choice"]))
