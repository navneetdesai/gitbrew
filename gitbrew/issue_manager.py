"""
Handler for issues
"""
import os
import subprocess
import sys

from PyInquirer import prompt

from gitbrew.gitpy import GitPy
from gitbrew.llms import OpenAI
from gitbrew.questions import Questions


class IssueManager:
    """
    Issue manager class
    """

    def __init__(self):
        """
        Initialize the issue manager

        openai_agent: OpenAI agent
        git_helper: GitPy object

        """
        # TOdo: setup the parameters
        self.openai_agent = OpenAI(
            os.getenv("OPENAI_API_KEY"),
            temperature=0.35,
            chat_model="gpt-4-1106-preview",
            frequency_penalty=0.6,
            max_tokens=64000,
        )
        self.git_helper = GitPy(os.getenv("GITHUB_TOKEN"))
        self.actions = {
            "List Issues": self._list_issues,
            "Create an Issue": self._create_issue,
            "Find Duplicate Issues": self._find_duplicate_issues,
            "Find Similar Issues": self._find_similar_issues,
            "Verify Issue Template": self._verify_issue_template,
            "Cancel": self.do_exit,
        }

    @staticmethod
    def do_exit(arg):
        """
        Handler for "exit" keyword
        :param arg: Optional args
        :return: True
        """
        return True

    def handle(self):
        """
        Handle issues

        Provide these functionalities
        1. List issues
            Remote, or custom
        2. Create issues
        3. Find duplicate issues in a repo
        4. Find similar issues before raising a new one
        5. Issue template verification?
        :return: None
        """
        url = self._get_repo_url()  # will be valid or throw an error
        user_intention = prompt(Questions.ISSUE_INTERACTION_QUESTIONS)["choice"]
        self.actions.get(user_intention, self.do_exit)(url)

    def _list_issues(self, state=open):
        """
        List issues

        :return: None
        """
        pass

    def _create_issue(self):
        """
        Create an issue

        :return: None
        """
        pass

    def _find_duplicate_issues(self):
        """
        Find duplicate issues

        :return: None
        """
        pass

    def _find_similar_issues(self):
        """
        Find similar issues

        :return: None
        """
        pass

    def _verify_issue_template(self):
        """
        Verify issue template

        :return: None
        """
        pass

    def _get_repo_url(self):
        """
        Get the repo url from the user or remote

        If user chooses remote, run git command using subprocess
        and returns a valid repo url as username/repo_name
        Otherwise prompts the user for the repo url
        :return: username/repo_name
        """
        questions = Questions.REPO_URL_QUESTIONS
        if prompt(questions)["repo_choice"] == "Remote":
            command = ["git", "remote", "get-url", "origin"]
            try:
                return (
                    subprocess.check_output(command, cwd=".", universal_newlines=True)
                    .strip()
                    .split(":")[1]
                    .split(".")[0]
                )
            except subprocess.CalledProcessError as e:
                print(f"Error: {e}")
                sys.exit(1)
        else:
            questions = Questions.ASK_FOR_REPO_URL
            url = prompt(questions)["repo_url"]
            return self.git_helper.extract_repo(url)
