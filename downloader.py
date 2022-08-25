"""Downloader Class for Requesting and Saving the data as gzip and text"""
import gzip
import os
import sys
from typing import Tuple
from urllib import parse

import bs4
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


class Downloader:
    def __init__(
        self,
        architecture: str,
        base_url: str,
        verbose: bool = True,
        file_name: str = "data",
    ):
        self.data_dir = "./repo_data"
        self.architecture = architecture
        self.gzip_filename = os.path.join(
            self.data_dir, (file_name + f"_{self.architecture}" + ".gz")
        )
        self.txt_filename = os.path.join(
            self.data_dir, (file_name + f"_{self.architecture}" + ".txt")
        )
        self.base_url = base_url
        self.base_pattern = "Contents-"
        self.verbosity = verbose

    def fetch_urls(self) -> list:
        """
        Fetch Content for all URLs from the Base URL

        Returns:
            list: all content-indices download urls

        """

        _, url_soup = Downloader._request_soup(self.base_url)
        return [
            link.get("href")
            for link in url_soup.find_all("a")
            if self.base_pattern in link.get("href")
        ]

    def fetch_arch_url(self) -> str:
        """
        Fetch URL for the given architecture

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
        Save data to gzip file

        Args:
            chunk_size: determines the packet size for streaming from url

        Returns:
            None
        """
        r, _ = Downloader._request_soup(self.fetch_arch_url())
        with open(self.gzip_filename, "wb") as f:
            if self.verbosity:
                with tqdm(
                    unit="B",
                    unit_scale=True,
                    unit_divisor=1024,
                    miniters=1,
                    desc="Downloading gzip",
                    total=int(r.headers.get("content-length", 0)),
                    bar_format="{l_bar}{bar:20}{r_bar}{bar:-10b}",
                    colour="green",
                ) as progress_bar:
                    for chunk in r.iter_content(chunk_size=chunk_size):
                        f.write(chunk)
                        progress_bar.update(len(chunk))
            for chunk in r.iter_content(chunk_size=chunk_size):
                f.write(chunk)

    def save_txt(self) -> None:
        """
        Save data as text

        Returns:
            None
        """
        with open(self.gzip_filename, "rb") as fr_gzip, open(
            self.txt_filename, "wb"
        ) as fr_txt:
            data = gzip.decompress(fr_gzip.read())
            fr_txt.write(data)

    def __str__(self):
        """
        Get architecture url

        Returns:
            str: architecture specific url
        """
        return f" For {self.architecture}, download URL - {self.fetch_arch_url()}"

    @staticmethod
    def _request_soup(url: str) -> Tuple[requests.Response, bs4.BeautifulSoup]:
        """
        Helper function: Prepare the Soup object for the URL after HTML Parsing

        Args:
            url: the link for making the request

        Returns:
            r: the response object from the request
            soup_object: the parsed content from the response

        """
        try:
            r = requests.get(url)
        except requests.exceptions.ConnectionError as e:
            sys.exit(e)
        else:
            return r, BeautifulSoup(r.text, "html.parser")
