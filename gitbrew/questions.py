"""
Questions prompts for pyinquirer
"""


class Questions:
    ISSUE_INTERACTION_QUESTIONS = [
        {
            "type": "list",
            "name": "choice",
            "message": "What would you like to do?",
            "choices": [
                "List Issues",
                "Create Issue",
                "Find Duplicate Issues",
                "Find Issues by Label",
                "Quit",
            ],
        }
    ]

    ISSUE_STATUS_QUESTIONS = [
        {
            "type": "list",
            "name": "choice",
            "message": "Do you want to filter the issues by status?",
            "choices": ["All issues", "Open issues", "Closed issues"],
        }
    ]

    REPO_URL_QUESTIONS = [
        {
            "type": "list",
            "name": "repo_choice",
            "message": "Which repository would you like to interact with?",
            "choices": ["Remote", "Custom"],
        }
    ]

    ASK_FOR_REPO_URL = [
        {
            "type": "input",
            "name": "repo_url",
            "message": "Enter the repository url",
        }
    ]
