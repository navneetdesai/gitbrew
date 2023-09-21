"""
Generates readme from a github repository
"""
import os

from dotenv import load_dotenv
from gitpy import GitPy
from llm.openai import OpenAI


def init():
    load_dotenv()
    github_token = os.getenv("GITHUB_TOKEN")
    openai_token = os.getenv("OPENAI_API_KEY")
    githandle = GitPy(token=github_token)
    llm = OpenAI(api_key=openai_token)
    return githandle, llm


def main():
    github, llm = init()
    # url = input("What's the repository url?: ")
    url = "https://github.com/navneetdesai/gitbrew/blob/main/LICENSE"

    repo = github.get_repo(url)
    contents = github.get_content(repo)
    print(contents)


if __name__ == "__main__":
    main()
