import pytest

from gitbrew.command_handler import CommandHandler
from gitbrew.exceptions import InvalidAnswerFormatException


@pytest.fixture
def command_handler():
    return CommandHandler()


@pytest.fixture
def show_recent_changes():
    return """<START>
    git show HEAD  
    <END>
    """


@pytest.fixture
def push_all_changes():
    return """<START>
    git add .
    <SEP>
    git commit -m "Create components for the UI."
    <SEP>
    git push origin    
    <END>
    """


@pytest.fixture()
def commands_with_clarifications():
    return """<START>
    git add .
    <SEP>
    git commit -m "Create components for the UI."
    <SEP>
    git push origin    
    <END>
    <CLARIFY>
    This will push all your local changes to the remote repository.
    </CLARIFY> 
    """


@pytest.fixture()
def invalid_llm_output():
    return """
    <END>
    
    <START>
    
    """


def test_one_command(command_handler, show_recent_changes):
    """
    LLM output has a single command, no sep, no clarifications
    Unit test: extract_commands
    """
    commands = command_handler.extract_commands(show_recent_changes)
    assert commands == command_handler.history[-1] == ["git show HEAD"]


def test_multiple_commands(command_handler, push_all_changes):
    """
    LLM output has multiple commands, has sep, no clarifications
    Unit test: extract_commands
    """
    commands = command_handler.extract_commands(push_all_changes)
    expected_commands = [
        "git add .",
        'git commit -m "Create components for the UI."',
        "git push origin",
    ]
    assert commands == command_handler.history[-1] == expected_commands


def test_command_with_clarification(command_handler, commands_with_clarifications):
    """
    LLM output has multiple commands, has sep, and clarifications
    Because of clarifications, no commands should be extracted for
    execution. History should be updated
    Unit test: extract_commands
    """
    commands = command_handler.extract_commands(commands_with_clarifications)
    assert commands == []
    assert command_handler.history[-1] == [
        "git add .",
        'git commit -m "Create components for the UI."',
        "git push origin",
    ]


def test_invalid_llm_response(command_handler, invalid_llm_output):
    """
    Unit test for execute_command
    Invalid answers returned by the LLM
    """
    with pytest.raises(InvalidAnswerFormatException):
        command_handler.extract_commands("""""")
    with pytest.raises(InvalidAnswerFormatException):
        command_handler.extract_commands(invalid_llm_output)


def test_clarification(command_handler):
    """
    Test input that prompts llm to ask for clarification
    :param command_handler:
    :return:
    """
    user_input = "what is the remote repository"
    llm_clarification = """<CLARIFY> 
        Are you asking for the URL or name of the remote repository in your git project? 
        </CLARIFY>"""
    command_handler.handle(user_input)
