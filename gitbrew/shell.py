import cmd
import subprocess


class Shell(cmd.Cmd):
    prompt = "gitbrew> "
    exit_keywords = ["exit", "quit"]

    @staticmethod
    def do_exit(arg):
        """
        Handler for "exit" keyword
        :param arg: Optional args
        :return: True
        """
        return True

    @staticmethod
    def do_quit(arg):
        """
        Handler for "quit" keyword
        :param arg: Optional args
        :return: True
        """
        return True

    # def do_help(self, arg: str) -> bool | None:
    #     # Todo: Add code to do_help
    #     pass

    def cmdloop(self, intro=None):
        """
        Create a command line loop
        :param intro: Intro
        :return: None
        """
        if intro:
            self.intro = intro
        try:
            super().cmdloop()
        except KeyboardInterrupt:
            print("\nExiting...")

    def do_gs(self, args):
        """
        List all subdirectories
        :param args:
        :return:
        """
        try:
            print(args)
            result = subprocess.run(
                ["git", "status"], capture_output=True, text=True, check=True
            )
            print(result.stdout)
        except subprocess.CalledProcessError as e:
            print("Oops! Something went wrong.\n", e)

    def default(self, line: str) -> None:
        """
        Handle text inputs from the user
        :param line:
        :return:
        """
        # ss1
        # print("Running `git remote -v`")
        # result = subprocess.run(
        #     ["git", "remote", "-v"], capture_output=True, text=True, check=True
        # )
        # print(result.stdout)

        # ss2
        print("Set alias gs = git status? (y/n)", end=": ")
        if input() == "y":
            print("Alias set gs=git status. Use gs to track files in the future!")
        else:
            pass
