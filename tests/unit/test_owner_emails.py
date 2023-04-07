import  cost_rules.owner_emails
from .fixtures.owner_rules import *
from .fixtures.owner_tags import *
from .fixtures.tag_names import *

import json
import os


def test_build_owner_rules():
    '''Test building rule list from tag list and account tags'''

    found_rules = cost_rules.owner_emails._build_owner_rules(
            expected_tag_list,
            expected_account_owners)

    assert found_rules == expected_owner_rules


def test_owner_emails_handler(mocker, apigw_event):
    # mock environment variables
    env_vars = {
        'OwnerEmailTagList': tag_list_string,
    }
    mocker.patch.dict(os.environ, env_vars)

    # mock out collect_account_tag_codes() with mock account tags
    mocker.patch('cost_rules.tag_client.collect_account_tags',
                 autospec=True,
                 return_value=expected_account_owners)

    # mock out build_rules() with mock rules
    mocker.patch('cost_rules.owner_emails._build_owner_rules',
                 autospec=True,
                 return_value=expected_owner_rules)

    # test event
    ret = cost_rules.owner_emails.lambda_handler(apigw_event, None)

    assert ret["body"] == json.dumps(expected_owner_rules)
    assert ret['statusCode'] == 200
