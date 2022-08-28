""" Tests for Command Line Parser Module"""

import pytest

from modules.cmdline_parser import args_parser, validate_arch


def test_validate_arch_valid(arch_valid):
    assert validate_arch(arch_valid) == arch_valid.lower()


def test_validate_arch_numeric(arch_numeric):
    with pytest.raises(TypeError):
        validate_arch(arch_numeric)


def test_cmdline_parser_arch(monkeypatch):
    monkeypatch.setattr("sys.argv", ["main.py", "alpha123", "-v"])
    assert args_parser().arch == "alpha123"
    assert args_parser().verbose
