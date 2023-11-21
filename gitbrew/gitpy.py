"""
Wrappers for the GitHub API
"""

from github import Github

from gitbrew import utilities
from gitbrew.constants import IgnoredFiles


class GitPy:
    def __init__(self, token, repo=None):
        """
        Initialize the GitPy object, repository (acc/repo)
        and optionally the repo object (from gitpy.get_repo)

        :param token: GitHub token
        :param repo: Repository string (acc/repo)
        """
        self.github: Github = Github(token)  # GitHub object
        self._repo_name: str = repo  # Repository string (acc/repo)
        self.repo = None  # Repository object

    def __repr__(self):
        """
        Representation of the GitPy object
        :return:
        """
        return f"GitPy(repo_str={self.repo_name})"

    def __str__(self):
        """
        String representation of the GitPy object
        :return:
        """
        return repr(self)

    @property
    def repo_name(self):
        """
        Repository string (acc/repo)
        :return:
        """
        return self._repo_name

    @repo_name.setter
    def repo_name(self, value):
        """
        Sets the repository string (acc/repo)
        :param value:
        :return:
        """
        self._repo_name = value

    def set_repo(self, repo_name=None):
        """
        Sets the GitPy repo object and the repository string (acc/repo)
        :param repo_name: Repository string (acc/repo)
        :return: None
        """
        if repo_name:
            self.repo_name = repo_name
            self.repo = self.github.get_repo(repo_name)
        elif self.repo_name:
            self.repo = self.github.get_repo(self.repo_name)
        else:
            raise ValueError("Repository name cannot be empty")

    def get_repo(self):
        """
        Gets a repository object from a url using github api
        :return: Repository object
        """
        if not self.repo:
            if not self.repo_name:
                raise ValueError("Repository name has not been set.")
            self.repo = self.github.get_repo(self.repo_name)
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
            if file_content.path.split(".")[-1] in IgnoredFiles.FILE_TYPES:
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
        :return: True if successful, False otherwise
        """
        repo = self.github.get_repo(self.repo_name)
        try:
            issue = repo.create_issue(*kwargs)
            print(f"Issue created successfully.\nURL: {issue.html_url}")
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False

    def list_issues(self, state="open"):
        """
        Lists all open issues in a repository by default
        :param state: open/closed/all
        :return:
        """
        issues = list(
            map(
                lambda x: (x.state, x.title, x.html_url), self.fetch_issues(state=state)
            )
        )
        utilities.print_table(
            issues, headers=["State", "Title", "URL"], show_index=True
        )

    def fetch_issues(self, **kwargs):
        """
        Fetches issues from a repository
        :param kwargs:  state, assignee, creator, mentioned, labels, sort, direction, since
        :return: issues
        """
        return self.repo.get_issues(**kwargs)

    def get_pull_requests(self, **kwargs):
        """
        Gets pull requests from a repository
        :param kwargs: state, head, base, sort, direction
        :return: pull requests
        """
        return self.repo.get_pulls(**kwargs)

    def get_pull_request(self, number):
        """
        Gets a pull request object from a repository by number
        :param number: pull request number
        :return: pull request object
        """
        return self.repo.get_pull(number)

    def get_issue(self, number):
        """
        Gets an issue object from a repository by number
        :param number: issue number
        :return: issue object
        """
        return self.repo.get_issue(number)
