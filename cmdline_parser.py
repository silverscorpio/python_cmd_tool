"""Command Line Parsing Using Argparse"""

import argparse


def validate_arch(arch: str) -> str:
    """
    Validate the 'arch' argument from cmdline assuming that no architecture
    is purely numeric and return the lowercase value if correct

    Args:
        arch: positional argument from cmd line

    Returns:
        str: the validated and converted to lowercase 'arch' argument

    """
    # TODO handle more gracefully
    if arch.isnumeric():
        raise TypeError("Invalid value for architecture")
    return arch.lower()


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
    args.arch = validate_arch(args.arch)
    return args
