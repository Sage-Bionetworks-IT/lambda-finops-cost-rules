import  cost_rules.chart_client
from .fixtures.chart import *

import pytest


def test_collect_chart(requests_mock):
    '''Test getting chart of accounts from lambda-mips-api'''

    # mock out requests call to get chart of accounts
    response_mock = requests_mock.get(chart_url, text=mock_chart_json)

    found_chart = cost_rules.chart_client.collect_chart_of_accounts(chart_url)
    assert found_chart == expected_chart_dict


def test_collect_chart_err(requests_mock):
    '''Test getting chart of accounts from lambda-mips-api'''

    invalid_url = "malformed"
    with pytest.raises(Exception):
        found_chart = cost_rules.chart_client.collect_chart_of_accounts(invalid_url)
