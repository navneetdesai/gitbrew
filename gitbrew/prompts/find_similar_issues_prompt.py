"""
! Currently unused
"""


class FindSimilarIssuesPrompt:
    FIND_SIMILAR_ISSUES_PROMPT = """
        Given a title and body of an issue, find similar issues.
        You will be given existing issues as a list of strings that have the title 
        and the body separated by a ':'. For example: Title: Body
        You will also be given a new issue, and you have to find the top 5 similar issues.
        This is the list of existing issues: {existing_issues}
        and this is the new issue: {new_issue}
    """
