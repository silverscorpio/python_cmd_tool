from downloader import Downloader
from parser import Parser


def main():
    # downloader = Downloader(architecture="amd64")
    # downloader.save_gzip()
    # downloader.save_txt()

    parser = Parser("data")
    parser.package_stats()


if __name__ == "__main__":
    main()
