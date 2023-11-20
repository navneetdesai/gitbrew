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
        pinecone.init(api_key=os.getenv("PINECONE_API_KEY"))
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
        all_embeddings = {
            issue.title: self.openai_agent.create_embedding(issue)
            for issue in all_issues
        }
        groups = self._generate_similarity_groups(all_embeddings, threshold)
        utilities.print_table(
            groups, headers=["Issue ID", "Similar Issues"], show_index=True
        )

    @staticmethod
    def _generate_similarity_groups(all_embeddings, threshold):
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
                    similar_issues.append((other_issue_id, similarity))
            similar_issues.sort(key=lambda x: x[1], reverse=True)
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
        new_issue_embedding = self.openai_agent.create_embedding(issue_text)
        issues = self.git_helper.fetch_issues(state="open")
        vectors = self.create_vectors(issues)
        self.upsert_embeddings(vectors, self.git_helper.repo_str)
        similar_issue_ids = self.query_db(embedding=new_issue_embedding, n=n)
        for id_ in similar_issue_ids:
            print(
                self.git_helper.repo.get_issue(id_["id"]).title,
                self.git_helper.repo.get_issue(id_["id"]).html_url,
            )

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

               {'matches': [{'id': 'C',
                    'score': 0.0,
                    'values': [0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3]},
                   {'id': 'D',
                    'score': 0.0799999237,
                    'values': [0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4]},
                   {'id': 'B',
                    'score': 0.0800000429,
                    'values': [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2]}],
        'namespace': ''}

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
            (issue.id, self._generate_embeddings(issue, issue_text)) for issue in issues
        ]

    def _generate_embeddings(self, issue, issue_text):
        issue_text = issue_text.format(issue.title, issue.body)
        issue_text = simple_preprocess(remove_stopwords(issue_text), deacc=True)
        return self.openai_agent.create_embedding(issue_text)
