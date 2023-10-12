"""
Wrappers for the GitHub API
"""
import re

from github import Auth, Github
from github.ContentFile import ContentFile


class GitPy:
    def __init__(self, token):
        self.repo = None
        self.github = Github(token)

    def get_repo(self, url):
        """
        Gets a repository object from a url
        :param url: Repository url
        :return: Repository object
        """
        self.repo = self.extract_repo(url)
        return self.github.get_repo(self.repo)

    @staticmethod
    def extract_repo(url):
        if match := re.search(r"github.com/([\w-]+)/([\w-]+)", url):
            if not match[1] or not match[2]:
                raise ValueError("Invalid repository url")
            return f"{match[1]}/{match[2]}"

    @staticmethod
    def get_content(repo):
        """
        Gets the contents of a repository
        :param repo: Repository object
        :return: List of contents as ContentFile objects
        """
        content = []
        contents = repo.get_contents("")
        while contents:
            file_content = contents.pop(0)
            # print(file_content.path.split('.')[-1])
            if file_content.path.split(".")[-1] in (
                "png",
                "jpg",
                "jpeg",
                "gif",
                "gitignore",
                "md",
                "txt",
            ):
                print(f"Skipping {file_content.path}")
                continue
            if file_content.type == "dir":
                contents.extend(repo.get_contents(file_content.path))
            else:
                content.append(file_content)
        return content
