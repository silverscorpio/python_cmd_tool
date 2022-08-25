"""Command Line Parsing Using Argparse"""

import argparse


def cmdline_parser():
    """
    Handle the Command Line Arguments

    Returns:
        args_object: the parsed arguments namespace

    """
    cmd_parser = argparse.ArgumentParser(
        description="Gets Debian Packages",
        prog="main script -> python main.py",
    )
    cmd_parser.add_argument(
        "arch",
        help="architecture for which debian packages are required",
    )
    cmd_parser.add_argument("-v", default=True, help="show progress bar for download")
    args = cmd_parser.parse_args()
    return args


if __name__ == "__main__":
    cmdline_parser()
