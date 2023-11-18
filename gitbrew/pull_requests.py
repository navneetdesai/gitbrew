"""
Handler class for pull request reviews
"""


import os
import re

from PyInquirer import prompt

from gitbrew.gitpy import GitPy
from gitbrew.llms import OpenAI
from gitbrew.prompts.pull_request_review_prompt import PullRequestReviewPrompt
from gitbrew.questions import Questions
from gitbrew.utilities import print_table


class PullRequestReviewer:
    """
    Pull request reviewer class
    """

    def __init__(self):
        """
        Initialize the pull request reviewer
        openai_agent: OpenAI agent
        git_helper: GitPy object
        actions: Actions that can be performed on user selection
        """
        self.openai_agent = OpenAI(
            os.getenv("OPENAI_API_KEY"),
            temperature=0.35,
            chat_model="gpt-4-1106-preview",
            frequency_penalty=0.6,
        )
        self.git_helper = GitPy(os.getenv("GITHUB_TOKEN"))
        self.actions = {
            "List pull requests": self._list_pull_requests,
            "Review a pull request": self._review_pull_request,
            "Exit": self._exit,
        }
        self.DEBUG = True
        self.NON_CODE_FILES = (
            ".txt",
            ".md",
            ".html",
            ".toml",
            ".lock",
            ".json",
            ".yml",
            ".yaml",
        )
        self.PULL_REQUEST_PATTERN = r"github.com/([\w-]+)/([\w-]+)/pull/([\d+])"
        self.HEADER = "# [GITBREW]: This is an auto-generated review. \n\n"

    def _exit(self):
        """
        Exit handler
        :return:
        """
        return

    def handle(self):
        """
        Handle for this class
        Should be called by the shell when the user wants to work with pull requests
        :return:
        """
        choice = prompt(Questions.PR_OPTIONS)["pr_option"]
        if selection := self.actions.get(choice):
            selection()

    def _list_pull_requests(self):
        """
        List all pull requests from a repo
        :return:
        """
        print_table(
            [
                [request.number, request.title, request.html_url]
                for request in self._fetch_pull_requests()
            ],
            headers=["Number", "Title", "URL"],
        )

    def _fetch_pull_requests(self, state="open"):
        """
        Fetch all pull requests from a repo
        Fetches only open PRs by default
        :param state: State of the pull request
        :return: List of pull requests
        """
        self.git_helper.repo_str = input("Enter the repository (user/repo): ")
        return self.git_helper.get_pull_requests(state=state)

    def _review_pull_request(self):
        """
        Review a pull request from a repo
        If the URL is valid, the review is posted to the pull request
        Otherwise exit with an error message
        :return:
        """
        url = input("Enter the pull request URL: ").strip()
        match = re.search(self.PULL_REQUEST_PATTERN, url)
        if not match:
            print("Invalid URL")
            return
        self.git_helper.repo_str = f"{match[1]}/{match[2]}"
        pull_request = self.git_helper.get_pull_request(int(match[3]))
        reviews = self.review(pull_request)  # reviews is a dict of filename: review
        self.DEBUG and print(f"REVIEW: {reviews}")
        self._post_review_with_confirmation(pull_request, reviews)

    def _post_review_with_confirmation(self, pull_request, reviews):
        """
        Ask user for confirmation before posting the review
        :param pull_request:
        :param reviews:
        :return:
        """
        question = Questions.REVIEW_CONFIRMATION
        if prompt(question)["confirmation"] == "Yes":
            self.post_review(reviews, pull_request)
        else:
            print("Review cancelled.")

    def review(self, pr):
        """
        Review a pull request
        Should be called by the shell when the user
        wants to review a pull request
        :return:
        """

        title, body, diff = pr.title, pr.body, pr.get_files()
        self.DEBUG and print("Reviewing PR: ", title)
        reviews = {}
        for file in diff:  # Get review for each file separately
            # Skip files non-code files
            if file.filename.endswith(self.NON_CODE_FILES):
                self.DEBUG and print("Skipping file: ", file.filename)
                continue
            self.create_review(body, file, reviews, title)
        return reviews

    def create_review(self, body, file, reviews, title):
        """
        Create a review for a file and add them to reviews dictionary

        :param body:
        :param file:
        :param reviews:
        :param title:
        :return:
        """
        content = file.patch
        self.DEBUG and print("Reviewing file: ", file.filename)
        _prompt = self.create_prompt(body, content, title)
        review = self.openai_agent.ask_llm(_prompt).replace("\n", "<br>")
        review = review.split("<br>")
        print(review)
        reviews[file.filename] = review

    @staticmethod
    def create_prompt(body, content, title):
        """
        Create and return the prompt for the pull request review
        from the PullRequestReviewPrompt template

        :param body:
        :param content:
        :param title:
        :return:
        """
        return [
            {
                "role": "user",
                "content": PullRequestReviewPrompt.template.format(
                    title=title, body=body, diff=content
                ),
            }
        ]

    def post_review(self, reviews, pull_request):
        """
        Post the review to the pull request on each file

        :param reviews: dict of filename: review
        :param pull_request: The pull request object
        :return: None
        """
        for file, review in reviews.items():
            review = "\n".join(review)
            pull_request.create_review(body=f"{self.HEADER}{review}", event="COMMENT")
            print(f"Review posted successfully for {file}.")
