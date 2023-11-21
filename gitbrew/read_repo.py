import os

import openai
from dotenv import load_dotenv

from gitbrew import utilities
from gitbrew.gitpy import GitPy


class CodeReader:
    def __init__(self, path):
        self.path = path
        self.code = None
        load_dotenv()
        github_token = os.getenv("GITHUB_TOKEN")
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.githandle = GitPy(token=github_token)
        self.repo = self.githandle.get_repo(utilities.extract_repo(self.path))
        self.files = self.githandle.get_content(self.repo)

    def read_repo(self):
        for file in self.files:
            if file.path.endswith(".py"):
                self.code = file.decoded_content.decode("utf-8")
                break


if __name__ == "__main__":
    path = input("Enter the path of the repository: ")
    reader = CodeReader(path)
    reader.read_repo()
