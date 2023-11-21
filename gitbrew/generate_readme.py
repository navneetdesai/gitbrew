"""
Generates readme from a github repository
"""
import base64
import os

from gitpy import GitPy
from llms.openai import OpenAI
from PyInquirer import prompt

from gitbrew import utilities
from gitbrew.constants import FILE_TYPES
from gitbrew.prompts.generate_readme_prompt import GenerateReadmePrompt
from gitbrew.prompts.summarize_file_prompt import SummarizeFilePrompt
from gitbrew.questions import Questions


class ReadmeGenerator:
    """
    Generates readme from a GitHub repository
    """

    def __init__(self, logger):
        self.git_helper = GitPy(os.getenv("GITHUB_TOKEN"))
        self.openai_agent = OpenAI(
            os.getenv("OPENAI_API_KEY"),
            temperature=0.4,
            chat_model="gpt-4-1106-preview",
            frequency_penalty=0.6,
            max_tokens=8000,
        )
        self.logger = logger

    def handle(self):
        """
        Entry point for the readme generator
        Should be called by the shell when the user wants to generate a readme.

        :return:
        """
        _prompt = Questions.README_INPUT_URL
        repo_url = prompt(_prompt)["repo_url"].strip()
        self.logger.info(f"Generating readme for {repo_url}")
        readme_content = self.generate_readme(repo_url)
        _prompt = Questions.README_FILE_NAME
        file_name = prompt(_prompt)["file_name"].strip()
        self._process_file_name(file_name)
        self.logger.info(f"Writing readme to {file_name}")
        self._write_readme(file_name, readme_content)

    @staticmethod
    def _write_readme(file_name, readme_content):
        """
        Writes the readme content to a file "README.md"
        in the current directory.
        If a file with the same name exists, it will be overwritten.
        :param readme_content: markdown content
        :return:
        """
        with open(file_name, "w") as f:
            f.write(readme_content)

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
        self.logger.info(f"Summarization prompt for {file}: {message[25:]}...")
        return self.openai_agent.ask_llm(message)

    def generate_readme(self, repo_url):
        """
        Generate the markdown content for the readme file
        :param repo_url: html url of the repository
        :return: markdown content as a string
        """
        # generate summaries for all files in the repo
        self.git_helper.set_repo(utilities.extract_repo(repo_url))
        repo = self.git_helper.get_repo()
        files = self.git_helper.get_content(repo)
        summaries = self.summarize_files(files)
        system_prompt = GenerateReadmePrompt.system_prompt
        user_prompt = GenerateReadmePrompt.user_prompt.format(
            summaries="\n\n".join(summaries)
        )
        message = self.openai_agent.create_message(system_prompt, user_prompt)
        return self.openai_agent.ask_llm(message)

    def _post_readme(self, repo_url, readme_content):
        """
        Push the readme to the repository root directory
        that does not have a readme.
        Pushes to the default branch of the repository.

        :param repo_url: html url of the repository
        :param readme_content: readme markdown content
        :return: None
        """
        pass  # currently not in the scope of the project

    @staticmethod
    def _process_file_name(file_name):
        """
        Process the file name
        :param file_name:
        :return:
        """
        if not file_name:
            return "README.md"
        if not file_name.contains("."):
            return file_name + ".md"
        return file_name
