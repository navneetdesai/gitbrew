"""
Generates readme from a github repository
"""
import os
from datetime import datetime

from dotenv import load_dotenv
from gitpy import GitPy
from llms.cohere import Cohere
from llms.openai import OpenAI

mock = True
# Todo: A lot of refactoring


def init():
    load_dotenv()
    github_token = os.getenv("GITHUB_TOKEN")
    openai_token = os.getenv("OPENAI_API_KEY")
    githandle = GitPy(token=github_token)
    # llm = OpenAI(api_key=openai_token)
    llm = Cohere()
    return githandle, llm


def main():
    github, llm = init()
    # url = input("What's the repository url?: ")
    url = "https://github.com/navneetdesai/ConnectFour"
    repo = github.get_repo(url)
    files = github.get_content(repo)
    print(files)

    if not mock:
        summaries = llm.summarize_file(files)
        with open(f"output/summaries-{datetime.now()}.md", "w") as f:
            f.write("\n".join(summaries))
    else:
        print("Mocking the summary generation")
        with open("output/summaries.md", "r") as f:
            summaries = f.readlines()

    readme_content = llm.generate_readme(summaries)
    print(readme_content)
    with open("Readme.md", "w") as f:
        f.write(readme_content)


if __name__ == "__main__":
    main()
