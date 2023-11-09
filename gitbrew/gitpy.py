"""
Wrappers for the GitHub API
"""
import re

from github import Auth, Github
from github.ContentFile import ContentFile


class GitPy:
    def __init__(self, token, repo=None, verbose=True):
        """
        Initialize the GitPy object, repository (acc/repo)
        and optionally the repo object (from gitpy.get_repo)
        :param token:
        :param repo:
        """
        self.repo_str: str = repo
        self.repo = None
        self.github: Github = Github(token)
        self.verbose = verbose

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

    def create_issue(self, *kwargs):
        """
        Creates an issue in a repository
        :param kwargs: title, body, assignee, labels
        :return: None
        """
        repo = self.github.get_repo(self.repo_str)
        repo.create_issue(*kwargs)
        print("Issue created successfully.")

    def list_issues(self, state="open"):
        """
        Lists all open issues in a repository by default
        :param state: open/closed/all
        :return:
        """
        issues = self.fetch_issues(state=state)
        for issue in issues:
            print(issue.title)
            print(issue.state)
            print("\n\n")

    def fetch_issues(self, **kwargs):
        repo = self.github.get_repo(self.repo_str)
        return repo.get_issues(**kwargs)

    def get_pull_requests(self, **kwargs):
        repo = self.github.get_repo(self.repo_str)
        return repo.get_pulls(**kwargs)
