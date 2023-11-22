import cmd
import sys

from PyInquirer import prompt
from questions import Questions
from rich.console import Console

from gitbrew.command_handler import CommandHandler
from gitbrew.generate_readme import ReadmeGenerator
from gitbrew.issue_manager import IssueManager
from gitbrew.pull_requests import PullRequestReviewer
from gitbrew.utilities import setup_logger


class Shell(cmd.Cmd):
    """
    Select one of the following options:
    1. Generate a Readme
        - Generate a readme for your repository
        - The application will ask you for the repository url and the path to the readme template
        - To aid the tool, you could create a draft readme with some information about your project

    2. Work with GitHub issues
        - Manage GitHub issues
           -  Find duplicate issues in a repository
           - Find similar issues in the repository before you create a new one
           -  Create a new issue from the terminal
    3. Use the git command line
        - Use git, but with natural language
        - Example - `Push all changes to the remote repository`
            You will be asked for confirmation before the command is executed
            Choose one of the following options for each command
            - Yes (Execute the command)
            - No (Abort the command)
            - Explain (Explains the command concisely)

            If the instruction is unclear, the application will ask for clarification.

            For better results, be as precise as possible.

    4. Review a pull request
        - Review pull requests
    5. Help
        - Read documentation
    6. Exit
        - Exits the application
    """

    prompt = "gitbrew> "
    exit_keywords = ["exit", "quit"]
    MESSAGE = "Welcome to gitbrew!\nEnter `help` for documentation. \nEnter `quit` or `exit` to exit the application.\n"

    def __init__(self):
        super().__init__()
        self.logger = setup_logger(save_logs=True, print_logs=True)
        self.command_handler = CommandHandler(self.logger)  # git command handler
        self.pull_request_reviewer = PullRequestReviewer(
            self.logger
        )  # pull request reviewer handler
        self.readme_generator = ReadmeGenerator(self.logger)  # readme generator handler
        self.issue_manager = IssueManager(self.logger)  # issue manager handler
        self.console = Console()
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
        sys.exit(0)

    def do_quit(self, arg=None):
        """
        Handler for "quit" keyword
        :param arg: Optional args
        :return: True
        """
        self.logger.info("Exiting...")
        sys.exit(0)

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
        if not arg:
            self.console.print(self.__doc__)
        self.cmdloop(intro=self.MESSAGE)

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
        self.preloop()

    def _readme_generation_handler(self):
        """
        Handler for readme generation
        :return:
        """
        self.logger.info("Calling readme generator...")
        self.readme_generator.handle()
        self.preloop()

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
        self.preloop()
