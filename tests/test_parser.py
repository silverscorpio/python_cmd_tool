""" Parser Test """
import pytest


@pytest.mark.parametrize(
    "unsorted_dict,sorted_dict_desc,sorted_dict_asc",
    [
        (
            {"a": range(1), "b": range(5), "c": range(3)},
            [("b", range(5)), ("c", range(3)), ("a", range(1))],
            [("a", range(1)), ("c", range(3)), ("b", range(5))],
        )
    ],
)
def test_parser_sort_dict_len_value(
    parser, unsorted_dict, sorted_dict_desc, sorted_dict_asc
):
    assert isinstance(parser.sort_dict_len_value(unsorted_dict), list)
    assert parser.sort_dict_len_value(unsorted_dict) == sorted_dict_asc
    assert parser.sort_dict_len_value(unsorted_dict, desc=True) == sorted_dict_desc


def test_parser_byte_to_str(parser, parser_byte_to_str):
    assert isinstance(parser.convert_to_str(parser_byte_to_str), str)


def test_parser_process_data(parser, parser_process_data):
    processed_dict = parser._process_data(parser_process_data)
    assert isinstance(processed_dict, dict)
    assert len(processed_dict["p1"]) == 1
    assert len(processed_dict["p2"]) == 2
    assert len(processed_dict["p3"]) == 3
    assert not processed_dict["p4"]
    assert "ungrouped_files" in processed_dict
    assert processed_dict["ungrouped_files"]
    assert processed_dict["ungrouped_files"] == ["f7"]
    assert processed_dict == {
        "p1": ["f1"],
        "p2": ["f2", "f4"],
        "p3": ["f3", "f5", "f6"],
        "p4": [],
        "ungrouped_files": ["f7"],
    }
