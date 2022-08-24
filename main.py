from parser import Parser

from downloader import Downloader


def main():
    """Requests, Downloads, Saves, Parses and Outputs the top-n packages"""

    # downloader = Downloader(architecture="amd64")
    # downloader.save_gzip()
    # downloader.save_txt()

    parser = Parser("data")
    parser.package_stats()


if __name__ == "__main__":
    # TODO add argparse with options for multiple architectures, help and error handling
    main()
