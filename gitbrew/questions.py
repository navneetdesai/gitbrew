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
                "Create an Issue",
                "Find Duplicate Issues",
                "Find Similar Issues",
                "Verify Issue Template",
                "Cancel",
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
            "message": "Enter the repository url: ",
        }
    ]

    USER_CONFIRMATION = [  # Get user confirmation before running git command
        {
            "type": "list",
            "name": "confirmation",
            "message": "We will run `{command}` Are you sure you want to proceed?",
            "choices": ["Yes", "No", "Explain"],
        }
    ]

    CHOOSE_UTILITY = [
        {
            "type": "list",
            "name": "utility",
            "message": "What would you like to do?",
            "choices": [
                "Generate a Readme",
                "Work with github issues",
                "Work with git",
                "Review a pull request",
                "Exit",
            ],
        }
    ]

    PR_OPTIONS = [
        {
            "type": "list",
            "name": "pr_option",
            "message": "What would you like to do?",
            "choices": [
                "List pull requests",
                "Review a pull request",
                "Exit",
            ],
        }
    ]

    REVIEW_CONFIRMATION = [
        {
            "type": "list",
            "name": "confirmation",
            "message": "We will post the review to the pull request. Are you sure you want to proceed?",
            "choices": ["Yes", "No"],
        }
    ]

    # Readme input URL
    README_INPUT_URL = [
        {
            "type": "input",
            "name": "repo_url",
            "message": "Enter the repository url: ",
        }
    ]

    # check whether the user wants to review the readme or post it
    README_FILE_NAME = [
        {
            "type": "input",
            "name": "file_name",
            "message": "What would you like to save the file as? ",
        }
    ]
