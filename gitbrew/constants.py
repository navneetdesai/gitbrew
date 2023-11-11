"""
List of commands
https://git-scm.com/docs/git
"""


class SafeCommands:
    """
    List of git commands that dont make changes
    """

    commands = {
        "status",
        "diff",
        "log",
        "remote",
        "tag",
        "show",
        "ls-files",
        "-v",
        "--version",
        "-h",
        "--help",
        "--html-path",
        "--man-path",
        "--info-path",
    }


class ConfigCommands:
    commands = {
        "-C",
        "-c",
        "--exec-path",
        "-p",
        "--paginate",
        "-P",
        "--no-pager",
        "--no-replace-objects",
        "--bare",
        "--git-dir",
        "--work-tree",
        "--namespace",
        "--super-prefix",
        "--config-env",
    }


class Commands:
    commands = {
        # start a working area
        "clone",
        "init",
        # work on current change
        "add",
        "am",
        "mv",
        "restore",
        "rm",
        # examine the history and state
        "bisect",
        "diff",
        "grep",
        "log",
        "show",
        "status",
        # grow, mark and tweak your common history
        "branch",
        "commit",
        "merge",
        "rebase",
        "reset",
        "switch",
        "tag",
        # collaborate
        "fetch",
        "pull",
        "push",
    }
