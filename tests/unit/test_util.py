import cost_rules.util
from .fixtures.tag_names import *


def test_parse_env_list():
    '''Test parsing TagList environment variable'''

    # assert expected tag list
    parsed_tag_list = cost_rules.util.parse_env_list(tag_list_string)
    assert parsed_tag_list == expected_tag_list


def test_strip_special_chars():
    '''Test removing unsafe characters from cost category names'''

    unsafe_name = 'foo & -bar'

    expected_safe_name = 'foo _ -bar'

    parsed_safe_name = cost_rules.util.strip_special_chars(unsafe_name)
    assert parsed_safe_name == expected_safe_name

def test_truncate_long_strings():
    '''Test truncating long names'''
    long_name = 'a really long string' + ('-' * 100)

    truncated_name = cost_rules.util.truncate_long_strings(long_name)
    assert len(truncated_name) == 42
