import cmd
import subprocess


class Shell(cmd.Cmd):
    prompt = "gitbrew> "

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
