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
    assert type(parser.sort_dict_len_value(unsorted_dict)) == list
    assert parser.sort_dict_len_value(unsorted_dict) == sorted_dict_asc
    assert parser.sort_dict_len_value(unsorted_dict, desc=True) == sorted_dict_desc
