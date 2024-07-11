"""Test suite for functions in the top-level module."""

from spond import is_list_of_dict


def test_is_list_of_dict__happy_path() -> None:
    # arrange
    data = [
        {"key0": 123},
        {"key1": "abc"},
    ]
    # act
    result = is_list_of_dict(data)
    # assert
    assert result is True


def test_is_list_of_dict__returns_false_if_input_is_none() -> None:
    # arrange
    test_data = None
    # act
    result = is_list_of_dict(test_data)
    # assert
    assert result is False
