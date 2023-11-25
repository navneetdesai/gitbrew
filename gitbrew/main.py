__package__ = "gitbrew"

from .shell import Shell


def main():
    shell = Shell()
    shell.cmdloop()


if __name__ == "__main__":
    main()
