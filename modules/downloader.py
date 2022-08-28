"""Downloader Class for Requesting and Saving the data as gzip and text"""

import gzip
import logging
import os
import sys
from typing import Tuple
from urllib import parse

import bs4
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

logger = logging.getLogger(__name__)


class Downloader:
    def __init__(
        self,
        architecture: str,
        base_url: str,
        verbose: bool,
        file_name: str = "data",
    ):
        self.data_dir = os.path.join(os.getcwd(), "files")
        self.architecture = architecture
        self.verbosity = verbose
        self.gzip_filename = os.path.join(
            self.data_dir, (file_name + f"_{self.architecture}" + ".gz")
        )
        self.txt_filename = os.path.join(
            self.data_dir, (file_name + f"_{self.architecture}" + ".txt")
        )
        self.base_url = base_url
        self.base_pattern = "Contents-"

    def fetch_urls(self) -> list:
        """
        Fetch and parse all download links of gzip files from base URL
        Returns:
            list: all download URLs
        """
        _, url_soup = Downloader.request_soup(self.base_url)
        return [
            link.get("href")
            for link in url_soup.find_all("a")
            if self.base_pattern in link.get("href")
        ]

    def extract_arch_url(self) -> str:
        """
        Extract URL for the given architecture from all URLs
        Returns:
            str: download url specific to the architecture
        """
        try:
            architecture_path = [
                link for link in self.fetch_urls() if self.architecture in link
            ][0]
        except IndexError:
            sys.exit("No file found for the given architecture")
        else:
            return parse.urljoin(self.base_url, architecture_path)

    def save_gzip(self, chunk_size: int = 1024) -> None:
        """
        Save data as a gzip file
        Args:
            chunk_size: determines the packet size for streaming from extracted URL
        Returns:
            None
        """
        if self.verbosity:
            logger.info("Downloading the File from URL as gzip...")
        r, _ = Downloader.request_soup(self.extract_arch_url())
        try:
            with open(self.gzip_filename, "wb") as f:
                with tqdm(
                    unit="B",
                    unit_scale=True,
                    unit_divisor=1024,
                    miniters=1,
                    desc="Progress",
                    total=int(r.headers.get("content-length", 0)),
                    bar_format="{l_bar}{bar:20}{r_bar}{bar:-10b}",
                    colour="green",
                ) as progress_bar:
                    for chunk in r.iter_content(chunk_size=chunk_size):
                        f.write(chunk)
                        progress_bar.update(len(chunk))
            for chunk in r.iter_content(chunk_size=chunk_size):
                f.write(chunk)
        except FileNotFoundError as e:
            sys.exit(e)

    def save_txt(self) -> None:
        """
        Save data (within gzip) in a text file
        Returns:
            None
        """
        if self.verbosity:
            logger.info("Saving as txt file for further use...")
        try:
            with open(self.gzip_filename, "rb") as fr_gzip, open(
                self.txt_filename, "wb"
            ) as fr_txt:
                data = gzip.decompress(fr_gzip.read())
                fr_txt.write(data)
        except FileNotFoundError as e:
            # TODO logging
            sys.exit(e)

    def __str__(self):
        """
        Give info about architecture url
        Returns:
            str: architecture url
        """
        return f" For {self.architecture}, download URL - {self.extract_arch_url()}"

    @staticmethod
    def request_soup(url: str) -> Tuple[requests.Response, bs4.BeautifulSoup]:
        """
        Helper function: Prepare Soup object for the URL after HTML Parsing
        Args:
            url: the link for making the request
        Returns:
            r: response object from the request
            soup_object: the parsed content from the response
        """
        # TODO status code handling with logging
        try:
            r = requests.get(url)
            r.raise_for_status()
        except requests.exceptions.HTTPError as e:
            sys.exit(f"HTTP Error: {e}")
        except requests.exceptions.ConnectionError as e:
            sys.exit(f"Cannot Connect: {e}")
        except requests.exceptions.RequestException as e:
            sys.exit(f"Other issue while making request: {e}")
        else:
            return r, BeautifulSoup(r.text, "html.parser")
