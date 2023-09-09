import pytest

from gitbrew.shell import Shell


@pytest.fixture
def shell():
    return Shell()


def test_exit_command(shell):
    assert shell.do_exit("") is True
    assert shell.do_exit("args") is True
    assert shell.do_quit("") is True
