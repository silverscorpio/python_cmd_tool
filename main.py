""" Main Script for Getting Debian Packages based on Architecture from Command Line with Python"""

import os

from modules.cmdline_parser import cmdline_parser
from modules.downloader import Downloader
from modules.logger import def_logger
from modules.parser import Parser


def main(url: str) -> None:
    """
    Request, Download, Save, Parse and Output the top-n Debian Packages
    Args:
        url: the base url for making request for downloading the contents
    Returns:
        None
    """

    # Get the architecture from command line
    args = cmdline_parser()

    # Download the data
    # downloader = Downloader(architecture=args.arch, base_url=url, verbose=args.v)
    # downloader.save_gzip()
    # downloader.save_txt()

    # Parse data and Output Package Statistics
    parser = Parser(architecture=args.arch, verbose=args.v)
    parser.package_stats(write_to_file=True)


if __name__ == "__main__":
    base_url = "http://ftp.uk.debian.org/debian/dists/stable/main/"
    logger = def_logger(log_dir=os.getcwd())
    main(base_url)
