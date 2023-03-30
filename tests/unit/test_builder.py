import cost_rules.builder
from .fixtures.basic_rules import *
from .fixtures.tag_names import *

def test_tag_rules():
    tag_rules = cost_rules.builder.build_tag_rules(mock_category, expected_tag_list, mock_tag_value)
    assert tag_rules == expected_tag_rules

def test_account_rule():
    account_rule = cost_rules.builder.build_account_rule(mock_category, expected_tag_list, mock_account_ids)
    assert account_rule == expected_account_rule

def test_inherit_rules():
    inherit_rules = cost_rules.builder.build_inherit_rules(expected_tag_list)
    assert inherit_rules == expected_inherit_rules
