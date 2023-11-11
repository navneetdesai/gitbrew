class ReadOnlyCommands:
    """
    List of git commands that dont make changes
    """

    commands = {
        "status",
        "log",
        "diff",
        "branch",
        "remote",
        "tag",
        "show",
        "ls-files",
    }
