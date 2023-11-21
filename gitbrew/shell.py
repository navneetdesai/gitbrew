import cmd
import sys

from PyInquirer import prompt
from questions import Questions

from gitbrew.command_handler import CommandHandler
from gitbrew.generate_readme import ReadmeGenerator
from gitbrew.issue_manager import IssueManager
from gitbrew.pull_requests import PullRequestReviewer
from gitbrew.utilities import setup_logger


class Shell(cmd.Cmd):
    prompt = "gitbrew> "
    exit_keywords = ["exit", "quit"]
    MESSAGE = "Welcome to gitbrew!\n Enter `help` for documentation. \nEnter `quit` or `exit` to exit the application.\n"

    def __init__(self):
        super().__init__()
        self.logger = setup_logger(save_logs=True, print_logs=True)
        self.command_handler = CommandHandler(self.logger)  # git command handler
        self.pull_request_reviewer = PullRequestReviewer(
            self.logger
        )  # pull request reviewer handler
        self.readme_generator = ReadmeGenerator(self.logger)  # readme generator handler
        self.issue_manager = IssueManager(self.logger)  # issue manager handler
        self.UTILITIES = {
            "Generate a Readme": self._readme_generation_handler,
            "Work with github issues": self._issue_manager_handler,
            "Use the git command line": self._git_command_handler,
            "Review a pull request": self._pull_request_handler,
            "Help": self.do_help,
            "Exit": self.do_exit,
        }

    def do_exit(self, arg=None):
        """
        Handler for "exit" keyword
        :param arg: Optional args
        :return: True
        """
        self.logger.info("Exiting...")
        return True

    def do_quit(self, arg=None):
        """
        Handler for "quit" keyword
        :param arg: Optional args
        :return: True
        """
        self.logger.info("Exiting...")
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

    def do_help(self, arg: str = ""):
        """
        Handler for "help" keyword
        :param arg: Optional args
        :return: True
        """
        self.logger.info("## Documentation ##")
        if arg:
            super().do_help(arg)
        else:
            ...

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
            print(f"I don't understand what you mean by: {line}.\n")
        questions = Questions.CHOOSE_UTILITY
        self.UTILITIES.get(prompt(questions)["utility"])()

    def _pull_request_handler(self):
        """
        Handler for pull requests
        :return:
        """
        self.logger.info("Calling pull request reviewer...")
        self.pull_request_reviewer.handle()

    def _readme_generation_handler(self):
        """
        Handler for readme generation
        :return:
        """
        self.logger.info("Calling readme generator...")
        self.readme_generator.handle()

    def _git_command_handler(self, line=None):
        """
        Handler for git commands
        :param line: git command
        :return: None
        """
        if not line:  # called by preloop
            return
        if line in self.exit_keywords:  # exit
            self.logger.info("Exiting from git command handler...")
            self.do_exit()
        self.logger.info("Calling git command handler...")
        self.command_handler.handle(line)  # handle git command

    def _issue_manager_handler(self):
        """
        Handler for issue manager
        :return: None
        """
        self.logger.info("Calling issue manager handler...")
        self.issue_manager.handle()
