""" Pytest Config - Defining fixtures etc."""

import pytest
from requests.exceptions import ConnectionError, HTTPError, RequestException

from modules.downloader import Downloader
from modules.parser import Parser


@pytest.fixture(params=["alpha123", "BETA456"])
def arch_valid(request):
    return request.param


@pytest.fixture
def arch_numeric():
    return "12345"


@pytest.fixture
def parser():
    return Parser(architecture="alpha123", verbose=False)


@pytest.fixture
def parser_byte_to_str():
    return b"alphaBetaCharlie"


@pytest.fixture
def downloader():
    return Downloader(
        architecture="alpha123", base_url="https://testurl", verbose=False
    )


class MockResponse:
    def __init__(self, response_status: int, response_text="alphabeta123"):
        self.status_code = response_status
        self.text = response_text

    def get_response_status(self):
        if self.status_code == 200:
            return self.status_code
        elif self.status_code // 100 == 4:
            return HTTPError
        elif self.status_code // 100 == 5:
            return ConnectionError
        else:
            return RequestException

    def raise_for_status(self):
        if self.status_code != 200:
            return HTTPError
