"""
Wrappers for the GitHub API
"""
import re

from github import Auth, Github
from github.ContentFile import ContentFile


class GitPy:
    def __init__(self, token, repo=None):
        """
        Initialize the GitPy object, repository (acc/repo)
        and optionally the repo object (from gitpy.get_repo)
        :param token:
        :param repo:
        """
        self.repo_str: str = repo
        self.repo = None
        self.github: Github = Github(token)

    @staticmethod
    def extract_repo(url):
        """
        Extracts the repository string (typically acc/repo)
         from a url
        :param url: github repo url
        :return: repository string as acc/repo
        """
        if match := re.search(r"github.com/([\w-]+)/([\w-]+)", url):
            if not match[1] or not match[2]:
                raise ValueError("Invalid repository url")
            return f"{match[1]}/{match[2]}"

    def get_repo(self, url):
        """
        Gets a repository object from a url using github api
        :param url: Repository url
        :return: Repository object
        """
        self.repo_str = self.extract_repo(url)
        self.repo = self.github.get_repo(self.repo_str)
        return self.repo

    @staticmethod
    def get_content(repo):
        """
        Gets the contents of a repository
        Feature: Readme generation
        :param repo: Repository object
        :return: List of contents as ContentFile objects
        """
        content = []
        contents = repo.get_contents("")
        while contents:
            file_content = contents.pop(0)
            # Todo: Add more file types
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

    def list_issues(self, status="open"):
        """
        Lists all open issues in a repository by default
        :param status: open/closed/all
        :return:
        """
        repo = self.github.get_repo(self.repo_str)
        open_issues = repo.get_issues(state="open")
        for issue in open_issues[:5]:
            print(issue.title)
            print(issue.state)
            print("\n\n")
