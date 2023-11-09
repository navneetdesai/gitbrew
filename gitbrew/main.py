from shell import Shell


def main():
    shell = Shell()
    shell.cmdloop(
        "Welcome to the utility! Enter `quit` or `exit` to exit the application."
    )


if __name__ == "__main__":
    main()
