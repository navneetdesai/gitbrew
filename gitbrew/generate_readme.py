"""
Generates readme from a github repository
"""
import base64
import os
from datetime import datetime

from dotenv import load_dotenv
from gitpy import GitPy
from llms.openai import OpenAI

from gitbrew.constants import FILE_TYPES
from gitbrew.prompts.generate_readme_prompt import GenerateReadmePrompt
from gitbrew.prompts.summarize_file_prompt import SummarizeFilePrompt


class ReadmeGenerator:
    """
    Generates readme from a github repository
    """

    def __init__(self):
        self.git_helper = GitPy(os.getenv("GITHUB_TOKEN"))
        self.openai_agent = OpenAI(
            os.getenv("OPENAI_API_KEY"),
            temperature=0.4,
            chat_model="gpt-4-1106-preview",
            frequency_penalty=0.6,
            max_tokens=8000,
        )

    def summarize_files(self, files):
        """
        Summarizes files
        :param files:
        :return:
        """
        return [
            f"File: {file}. \n Summary: {self._summarize_file(file)}"
            for file in files
            if self._to_summarize(file)
        ]

    @staticmethod
    def _to_summarize(file):
        """
        Returns true if the file should be summarized
        :param file:
        :return:
        """
        return any(file.name.endswith(_type) for _type in FILE_TYPES.FILE_TYPES)

    def _summarize_file(self, file):
        """
        Summarizes a file using SummarizeFilePrompt
        and the openai agent chat endpoint
        :param file: GitHub file object
        :return: summary of the file
        """
        system_prompt = SummarizeFilePrompt.system_prompt
        user_prompt = SummarizeFilePrompt.user_prompt.format(
            filename=file, content=base64.b64decode(file.content).decode("utf-8")
        )
        message = self.openai_agent.create_message(system_prompt, user_prompt)
        return self.openai_agent.ask_llm(message)

    def generate_readme(self, repo_url):
        """
        Generate the markdown content for the readme file
        :param repo_url: html url of the repository
        :return: markdown content as a string
        """
        # generate summaries for all files in the repo
        repo = self.git_helper.get_repo(repo_url)
        files = self.git_helper.get_content(repo)
        summaries = self.summarize_files(files)
        system_prompt = GenerateReadmePrompt.system_prompt
        user_prompt = GenerateReadmePrompt.user_prompt.format(
            summaries="\n\n".join(summaries)
        )
        message = self.openai_agent.create_message(system_prompt, user_prompt)
        return self.openai_agent.ask_llm(message)
