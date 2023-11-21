"""
Handler for issues
"""
import os
import subprocess
import sys

import pinecone
from gensim.parsing.preprocessing import remove_stopwords
from gensim.utils import simple_preprocess
from PyInquirer import prompt
from sklearn.metrics.pairwise import cosine_similarity

from gitbrew import utilities
from gitbrew.gitpy import GitPy
from gitbrew.llms import OpenAI
from gitbrew.questions import Questions


class IssueManager:
    """
    Issue manager class
    """

    CHOICES = {"All issues": "all", "Open issues": "open", "Closed issues": "closed"}

    def __init__(self):
        """
        Initialize the issue manager

        openai_agent: OpenAI agent
        git_helper: GitPy object

        """
        self.openai_agent = OpenAI(
            os.getenv("OPENAI_API_KEY"),
            embeddings_model="text-embedding-ada-002",
        )

        self.git_helper = GitPy(os.getenv("GITHUB_TOKEN"))
        pinecone.init(api_key=os.getenv("PINECONE_API_KEY"), environment="us-east1-gcp")
        self.pinecone_index = pinecone.Index("gitbrew")
        self.actions = {
            "List Issues": self._list_issues,
            "Create an Issue": self._create_issue,
            "Find Duplicate Issues": self._find_duplicate_issues,
            "Find Similar Issues": self._find_similar_issues,
            "Cancel": self.exit,
        }

    def __del__(self):
        pass

    @staticmethod
    def exit(arg):
        """
        Handler for "exit" keyword
        :param arg: Optional args
        :return: True
        """
        return True

    def handle(self):
        """
        Handle issues
        Loops until user chooses to cancel/exit

        repo options: remote or custom

        Provide these functionalities
        1. List issues
        2. Create issues
        3. Find duplicate issues in a repo
        4. Find similar issues before raising a new one
        :return: None
        """
        self.git_helper.repo_str = (
            self._get_repo_url()
        )  # will be valid or throw an error
        user_intention = prompt(Questions.ISSUE_INTERACTION_QUESTIONS)["choice"]
        while user_intention != "Cancel":
            self.actions.get(user_intention, self.exit)()
            user_intention = prompt(Questions.ISSUE_INTERACTION_QUESTIONS)["choice"]

    def _list_issues(self, state=open):
        """
        List issues. Default state is open.

        :return: None
        """
        questions = Questions.ISSUE_STATUS_QUESTIONS
        state = self.CHOICES.get(prompt(questions)["choice"])
        self.git_helper.list_issues(state)

    def _create_issue(self):
        """
        Create an issue in the repository
        Prompts for title and body and
        creates an issue using the gitpy module
        without any further user interaction

        :return: None
        """
        title, body = self._get_issue_description()
        self.git_helper.create_issue(title, body)

    def _find_duplicate_issues(self, threshold=0.75):
        """
        Group duplicate issues in the repository

        :return: None
        """
        all_issues = self.git_helper.fetch_issues(state="open")
        issue_text = "Title: {title}\n Body: {body}"
        all_embeddings = {
            issue.number: self.openai_agent.create_embedding(
                issue_text.format(title=issue.title, body=issue.body)
            )["data"][0]["embedding"]
            for issue in all_issues
        }
        groups = self._generate_similarity_groups(all_embeddings, threshold)
        utilities.print_dictionary(groups, headers=["Title", "URL", "Similarity"])

    def _generate_similarity_groups(self, all_embeddings, threshold):
        """
        Generate similarity groups for duplicate issues
        :param all_embeddings:
        :param threshold:
        :return:
        """
        groups = {}
        items = all_embeddings.items()
        for issue_id, embed in items:
            similar_issues = []
            for other_issue_id, other_embed in items:
                if issue_id == other_issue_id:
                    continue
                similarity = cosine_similarity([embed], [other_embed])[0][0]
                if similarity > threshold:
                    issue = self.git_helper.get_issue(other_issue_id)
                    similar_issues.append((issue.title, issue.html_url, similarity))
            similar_issues.sort(key=lambda x: x[2], reverse=True)
            groups[issue_id] = similar_issues
        return groups

    def _find_similar_issues(self, n=10):
        """
        Finds similar issues that have been raised in the repository.
        Uses OpenAI's semantic search to find similar issues
        to avoid duplication.
        To be used before creating a new issue

        :return: None
        """
        title, body = self._get_issue_description()
        issue_text = f"Title: {title}\n Body: {body}"
        new_issue_embedding = self.openai_agent.create_embedding(issue_text)["data"][0][
            "embedding"
        ]
        issues = self.git_helper.fetch_issues(state="open")
        vectors = self.create_vectors(issues)
        self.pinecone_index.delete(delete_all=True, namespace=self.git_helper.repo_str)
        self.upsert_embeddings(vectors, self.git_helper.repo_str)
        similar_issue_ids = self.query_db(embedding=new_issue_embedding, n=n)
        repo = self.git_helper.github.get_repo(self.git_helper.repo_str)
        data = [
            (
                repo.get_issue(int(id_["id"])).title,
                repo.get_issue(int(id_["id"])).html_url,
            )
            for id_ in similar_issue_ids
        ]
        utilities.print_table(data, headers=["Title", "URL"], show_index=True)

    def _get_repo_url(self):
        """
        Get the repo url from the user or remote

        If user chooses remote, run git command using subprocess
        and returns a valid repo url as username/repo_name
        Otherwise prompts the user for the repo url
        :return: username/repo_name
        """
        questions = Questions.REPO_URL_QUESTIONS
        if prompt(questions)["repo_choice"] == "Remote":
            command = ["git", "remote", "get-url", "origin"]
            try:
                return (
                    subprocess.check_output(command, cwd=".", universal_newlines=True)
                    .strip()
                    .split(":")[1]
                    .split(".")[0]
                )
            except subprocess.CalledProcessError as e:
                print(f"Error: {e}")
                sys.exit(1)
        else:
            questions = Questions.ASK_FOR_REPO_URL
            url = prompt(questions)["repo_url"]
            return self.git_helper.extract_repo(url)

    @staticmethod
    def _get_issue_description():
        """
        Get the issue title and description from the user
        :return: title, body
        """
        title = input("What's the title of the new issue? ")
        body = input("What's the description the new issue? ")
        return title, body

    def query_db(self, embedding, n):
        """
        Query the database for similar issues

        :param embedding: new issue embedding
        :param n: number of similar issues to return
        :return: list of similar issues
        """
        response = self.pinecone_index.query(
            namespace=self.git_helper.repo_str,
            top_k=n,
            vector=embedding,
        )
        return response["matches"]

    def upsert_embeddings(self, vectors, namespace):
        """
        Upsert the embedding for an issue into the database

        :param vectors: list of vectors
        :param namespace: namespace

        :return: None
        """
        self.pinecone_index.upsert(
            vectors=vectors,
            namespace=namespace,
        )

    def create_vectors(self, issues):
        """
        Create vectors for a list of issues

        :param issues: list of issues
        :return: list of vectors
        """
        issue_text = "Title: {title}\n Body: {body}"
        return [
            (str(issue.number), self._generate_embeddings(issue, issue_text))
            for issue in issues
        ]

    def _generate_embeddings(self, issue, issue_text):
        print("Checking issue:", issue.title)
        issue_text = issue_text.format(title=issue.title, body=issue.body)
        issue_text = simple_preprocess(remove_stopwords(issue_text), deacc=True)
        return self.openai_agent.create_embedding(issue_text)["data"][0]["embedding"]