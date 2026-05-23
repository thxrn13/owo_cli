import os
import argparse
import subprocess


def main() -> None:
    """
    Setup function for owo_pwease. Reads command line arguments on posix systems and updates shell profile.
    :return: None
    """

    # Initialize arg_parser
    arg_parser = argparse.ArgumentParser()

    # Posix
    if os.name == 'posix':
        # Get shell and set default filepath
        shell = os.getenv('SHELL').split('/')[-1]
        shell_file_name = os.path.expanduser('~/.{}rc'.format(shell))

        # Read filepath fom cl arguments
        arg_parser.add_argument('-sf', '--shell_file',
                                required=False,
                                action='store',
                                help="path to shell profile. defaults to {}".format(shell_file_name)
                                )

        # Set filepath if one is provided
        args = arg_parser.parse_args()
        shell_file_arg = args.shell_file
        if shell_file_arg is not None:
            shell_file_name = shell_file_arg

        # open shell profile and add aliases
        with open(shell_file_name, 'a') as f:
            lines = ["# >>> owo/owo >>>\n",
                     "alias owo=thefuck\n",
                     "alias owo='sudo $(fc -ln -1)'\n",
                     "# <<< owo/owo <<<\n"]
            if os.name == 'posix':
                f.write("\n\n")
                f.writelines(lines)

        # prompt user to refresh
        print("restart shell or run \n\n\tsource {}\n\nfor changes to take effect".format(shell_file_name))

    # Windows
    elif os.name == 'nt':
        # fet $PROFILE path
        profile = subprocess.run(["powershell", "-Command", "$PROFILE"], capture_output=True, text=True)\
            .stdout.strip()

        # open profile file and update aliases
        with open(profile, 'a') as f:
            f.write('\n\niex "$(thefuck --alias owo)"\n')

            # prompt user to refresh
            print('restart shell or run \n\n\t. $PROFILE\n\nfor changes to take effect')


if __name__ == '__main__':
    main()
