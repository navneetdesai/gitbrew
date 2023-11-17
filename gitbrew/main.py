import sys

from rich.console import Console
from shell import Shell


def main():
    shell = Shell(debug=len(sys.argv) > 1 and sys.argv[1] == "--debug")
    shell.cmdloop()


if __name__ == "__main__":
    main()
