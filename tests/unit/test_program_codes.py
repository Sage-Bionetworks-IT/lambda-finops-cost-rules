import os

import cost_rules.program_codes
from .fixtures.chart import *
from .fixtures.code_rules import *
from .fixtures.code_tags import *
from .fixtures.tag_names import *


def test_build_program_rules():
    """
    Test building rule list from tag list and account tags
    """

    found_rules = cost_rules.program_codes._build_program_rules(
        expected_chart_dict, expected_tag_list, expected_account_codes
    )

    assert found_rules == expected_program_rules


def test_program_codes_handler(mocker, apigw_event):
    # mock environment variables
    env_vars = {
        "ChartOfAccountsURL": chart_url,
        "ProgramCodeTagList": tag_list_string,
    }
    mocker.patch.dict(os.environ, env_vars)

    # mock out collect_account_tag_codes() with mock account tags
    mocker.patch(
        "cost_rules.tag_client.collect_account_tags",
        autospec=True,
        return_value=expected_account_codes,
    )

    # mock out collect_chart_of_accounts() with mock chart of account
    mocker.patch(
        "cost_rules.chart_client.collect_chart_of_accounts",
        autospec=True,
        return_value=expected_chart_dict,
    )

    # mock out build_rules() with mock rules
    mocker.patch(
        "cost_rules.program_codes._build_program_rules",
        autospec=True,
        return_value=expected_program_rules,
    )

    # mock out write_rules_to_s3()
    mocker.patch("cost_rules.s3_client.write_rules_to_s3", autospec=True)

    # test event
    ret = cost_rules.program_codes.lambda_handler(apigw_event, None)

    assert ret["statusCode"] == 201
