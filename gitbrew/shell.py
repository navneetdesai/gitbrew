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
from gitbrew.llms import OpenAI
from gitbrew.prompts.pull_request_review_prompt import PullRequestReviewPrompt
from gitbrew.pull_requests import PullRequestReviewer


class Shell(cmd.Cmd):
    prompt = "gitbrew> "
    exit_keywords = ["exit", "quit"]
    CHOICES = {"All issues": "all", "Open issues": "open", "Closed issues": "closed"}

    def do_1(self, arg):
        """
        Unit testing shortcut - to be deleted
        :return:
        """
        # self.git_helper.repo_str = "https://github.com/Textualize/rich"
        # self.git_helper.repo_str = "Textualize/rich"
        # self.do_issue_interaction()
        # self.pr_review_comment()
        ...

    def __init__(self, debug=False):
        super().__init__()
        load_dotenv()
        self.openai_agent = OpenAI(os.getenv("OPENAI_API_KEY"), temperature=0.35)
        self.DEBUG = debug
        self.git_helper = GitPy(os.getenv("GITHUB_TOKEN"))
        self.pull_request_reviewer = PullRequestReviewer()
        self.embeddings_cache = {}
        self.command_handler = CommandHandler(debug=self.DEBUG)
        self.console = Console()

    def completedefault(self, text, line, begidx, endidx):
        # Customize the completion logic here
        # Return a list of possible completions for 'text'
        possible_completions = ["apple", "banana", "cherry", "dog", "elephant"]
        return [
            completion
            for completion in possible_completions
            if completion.startswith(text)
        ]

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
            self.command_handler.handle(line)
            # raise AttributeError(f"Unknown command: {line}")

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
                print(f"Target repository: {self.git_helper.repo_str}")
                url = result.strip()
                # Todo: Needs to be better designed
                repo = url.split(":")[1].split(".")[0]
                # self.git_helper.repo_str = repo
            except subprocess.CalledProcessError as e:
                print(f"Error: {e}")
                sys.exit(1)
        else:
            # url = https://github.com/quora/pyanalyze # for testing
            questions = Questions.ASK_FOR_REPO_URL
            url = prompt(questions)["repo_url"]
            self.git_helper.repo_str = self.git_helper.extract_repo(url)

        questions = Questions.ISSUE_INTERACTION_QUESTIONS
        answers = prompt(questions)
        choice = answers["choice"]

        if choice == "List Issues":
            self._list_issues()
        elif choice == "Create Issue":
            self._create_issue()
        elif choice == "Find Duplicate Issues":
            duplicate_issues = self._retrieve_duplicate_issues(
                self._prompt_title_body()
            )
            for issue in duplicate_issues:
                print(issue)
        elif choice == "Find Issues by Label":
            label = input("Enter the label: ")
            issues = self.git_helper.fetch_issues(labels=[label])
            for issue in issues:
                print(issue.title, issue.url, sep=": ")
        elif choice == "Cancel":
            print("Cancelling...")
            return

    def _list_issues(self):
        """
        Lists issues in a repository based on status
        Default status: open
        Status can be: open, closed, all
        :return:
        """
        questions = Questions.ISSUE_STATUS_QUESTIONS
        self.git_helper.list_issues(self.CHOICES.get(prompt(questions)["choice"]))

    def _retrieve_duplicate_issues(self, title=None, body=None, n=10):
        """
        Returns top 10 open issues that are most likely to be similar to the new issue
        :param title: Title of the new issue
        :param body: Body of the new issue
        :return: List of duplicate issues (top 10)
        """
        open_issues = self.git_helper.fetch_issues(state="open")
        issue_text = [f"{issue.title}: {issue.body[:1000]}" for issue in open_issues]
        new_issue_text = f'{title or ""}: {body or ""}'
        indices: list[tuple[int, Any]] = self._find_similar_issues_openai(
            new_issue_text, issue_text, n
        )

        return [
            f"{open_issues[index[0]].title}:{open_issues[index[0]].html_url}"
            for index in indices
        ]

    def _create_issue(self):
        """
        Create an issue from the command line
        :return:
        """
        body, title = self._prompt_title_body()
        yn = input(
            "Would you like to check if this issue has already been raised? (y/n): "
        )
        duplicate_issues = self._retrieve_duplicate_issues(title, body)
        if yn == "y" and duplicate_issues:
            print("Possible duplicate issues found:")
            for issue in duplicate_issues:
                print(issue)
        yn = input("Would you like to create this issue? (y/n): ")
        if yn == "y":
            self.git_helper.create_issue(title, body)
        else:
            print("Issue not created")

    @staticmethod
    def _prompt_title_body():
        title = input("What's the title of the new issue? ")
        body = input("What's the description the new issue? ")
        title = "Add validation for strings using regular expressions"
        body = "We could add more robustness to user input validation by creating a class that uses reg expr"
        return body, title

    def triage_issue(self):
        """
        Triage issues
        :return:
        """
        pass

    def _find_similar_issues_openai(self, new_issue_text, issue_text, n=10):
        """
        Find similar issues based on cosine similarity
        :param new_issue_text:
        :param issue_text:
        :return:
        """
        if self.git_helper.repo_str in self.embeddings_cache:
            print("Using cached embeddings")
            embeddings = self.embeddings_cache[self.git_helper.repo_str]
        else:
            # print("Generating embeddings")
            embeddings = self.embeddings_cache[
                self.git_helper.repo_str
            ] = openai.Embedding.create(
                input=issue_text,
                model="text-embedding-ada-002",
            )
        new_issue_embedding = openai.Embedding.create(
            input=new_issue_text,
            model="text-embedding-ada-002",
        )
        y = new_issue_embedding["data"][0]["embedding"]
        scores = []
        for index, embedding in enumerate(embeddings["data"]):
            x = embedding["embedding"]
            similarity = cosine_similarity([x], [y])[0][0]
            scores.append((index, similarity))

        return sorted(scores, reverse=True, key=lambda m: m[1])[:n]

    def review_pull_request(self):
        """
        Review a pull request
        Should be called by the shell when the user
        wants to review a pull request
        :return:
        """
        pull_requests = self.git_helper.get_pull_requests()
        pr = pull_requests[0]
        title, body, diff = pr.title, pr.body, pr.get_files()
        print("Reviewing PR: ", title)
        diff = "\n".join([file.patch for file in diff])
        _prompt = [
            {
                "role": "user",
                "content": PullRequestReviewPrompt.template.format(
                    title=title, body=body, diff=diff
                ),
            }
        ]
        review = self.openai_agent.ask_llm(_prompt)
