import requests
from bs4 import BeautifulSoup
import gzip
from urllib import parse
from tqdm import tqdm


class Downloader:
    def __init__(self, architecture: str = "", file_name: str = "data"):
        self.gzip_filename = file_name + ".gz"
        self.txt_filename = file_name + ".txt"
        self.architecture = architecture
        self.base_url = "http://ftp.uk.debian.org/debian/dists/stable/main/"
        self.base_pattern = "Contents-"

    def fetch_urls(self) -> list:
        _, url_soup = Downloader.request_soup(self.base_url)
        return [
            link.get("href")
            for link in url_soup.find_all("a")
            if self.base_pattern in link.get("href")
        ]

    def fetch_arch_url(self) -> str:
        if self.architecture:
            architecture_path = [
                link for link in self.fetch_urls() if self.architecture in link
            ]
            return parse.urljoin(self.base_url, architecture_path[0])

    def save_gzip(self, chunk_size: int = 1024) -> None:
        r, _ = Downloader.request_soup(self.fetch_arch_url())
        with open(self.gzip_filename, "wb") as f:
            with tqdm(
                unit="B",
                unit_scale=True,
                unit_divisor=1024,
                miniters=1,
                desc="Downloading gzip",
                total=int(r.headers.get("content-length", 0)),
            ) as progress_bar:
                for chunk in r.iter_content(chunk_size=chunk_size):
                    f.write(chunk)
                    progress_bar.update(len(chunk))

    def save_txt(self) -> None:
        with open(self.gzip_filename, "rb") as fr_gzip, open(
            self.txt_filename, "wb"
        ) as fr_txt:
            data = gzip.decompress(fr_gzip.read())
            fr_txt.write(data)

    def __str__(self):
        if self.architecture:
            return f" For {self.architecture}, download URL - {self.fetch_arch_url()}"
        return f"All File URLs - {self.fetch_urls()}"

    @staticmethod
    def request_soup(url: str):
        # TODO implement exceptions
        r = requests.get(url)
        return r, BeautifulSoup(r.text, "html.parser")
