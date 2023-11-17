import os
import sys

import openai
from dotenv import load_dotenv

from gitbrew.gitpy import GitPy
from gitbrew.prompts.pull_request_review_prompt import PullRequestReviewPrompt


class PullRequestReviewer:
    def __init__(self, openai_agent, pr_url=None, repo=None):
        self.pr_url = pr_url
        self.repo = repo
        self.openai_agent = openai_agent
        self.git_helper = GitPy(os.getenv("GITHUB_TOKEN"))

    def review(self):
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


if __name__ == "__main__":
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")
    if len(sys.argv) < 2:
        print("Usage: python3 pull_requests.py <repo_url>")
        sys.exit(1)
    url = sys.argv[1]
    reviewer = PullRequestReviewer(url)
    reviewer.review()
