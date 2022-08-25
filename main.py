""" Main Script for Getting Debian Packages based on Architecture from Command Line with Python"""

from parser import Parser

from cmdline_parser import cmdline_parser
from downloader import Downloader


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
    downloader = Downloader(architecture=args.arch, base_url=url, verbose=args.v)
    downloader.save_gzip()
    downloader.save_txt()

    # Parse data and Output Package Statistics
    parser = Parser("data")
    parser.package_stats()


if __name__ == "__main__":
    # TODO add argparse with options for multiple architectures, help and error handling
    base_url = "http://ftp.uk.debian.org/debian/dists/stable/main/"
    main(base_url)
