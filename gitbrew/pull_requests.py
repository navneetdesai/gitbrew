import os
import sys

import openai
from dotenv import load_dotenv


class PullRequestReviewer(object):
    def __init__(self, pr_url=None, repo=None):
        self.pr_url = pr_url
        self.repo = repo

    def review(self):
        pass


if __name__ == "__main__":
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")
    if len(sys.argv) < 2:
        print("Usage: python3 pull_requests.py <repo_url>")
        sys.exit(1)
    url = sys.argv[1]
    reviewer = PullRequestReviewer(url)
    reviewer.review()
