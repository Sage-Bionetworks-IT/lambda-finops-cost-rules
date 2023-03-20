import cost_rules.app

import json
import os

import boto3
import pytest
from botocore.stub import Stubber


# injected env var value
tag_list_string = 'TagOne,TagTwo'

# expected parsed env var value
expected_tag_list = [ 'TagOne', 'TagTwo' ]

# mock return for list_accounts()
mock_account_list = {
    'Accounts': [
        { 'Id': '111222333444', },
        { 'Id': '222333444555', },
        { 'Id': '333444555666', },
    ]
}

# mock return for list_tags_for_resource()
mock_resource_tags_a = {
    'Tags': [
        {
            'Key': 'TagOne',
            'Value': "Program Part A / 123456",
        },
    ]
}

# mock return for list_tags_for_resource()
mock_resource_tags_b = {
    'Tags': [
        {
            'Key': 'TagOne',
            'Value': "Program Part B / 123456",
        },
    ]
}

# mock return for list_tags_for_resource()
mock_resource_tags_other = {
    'Tags': [
        {
            'Key': 'TagTwo',
            'Value': "Other Program / 654321",
        },
    ]
}

# expected account code dictionary
expected_account_codes = {
    '123456': [
        '111222333444',
        '333444555666',
    ],
    '654321': [
        '222333444555',
    ],
}

# injected env var value
chart_url = 'https://example.com/path'

# mock chart of accounts returned from `lambda-mips-api`
mock_chart_json = '''{
"000000": "No Program",
"000001": "Other",
"123456": "Program Part A",
"654321": "Other Program"
}'''

expected_rules = ''

@pytest.fixture()
def apigw_event():
    """ Generates API GW Event"""

    return {
        "body": '{ "test": "body"}',
        "resource": "/{proxy+}",
        "requestContext": {
            "resourceId": "123456",
            "apiId": "1234567890",
            "resourcePath": "/{proxy+}",
            "httpMethod": "POST",
            "requestId": "c6af9ac6-7b61-11e6-9a41-93e8deadbeef",
            "accountId": "123456789012",
            "identity": {
                "apiKey": "",
                "userArn": "",
                "cognitoAuthenticationType": "",
                "caller": "",
                "userAgent": "Custom User Agent String",
                "user": "",
                "cognitoIdentityPoolId": "",
                "cognitoIdentityId": "",
                "cognitoAuthenticationProvider": "",
                "sourceIp": "127.0.0.1",
                "accountId": "",
            },
            "stage": "prod",
        },
        "queryStringParameters": {"foo": "bar"},
        "headers": {
            "Via": "1.1 08f323deadbeefa7af34d5feb414ce27.cloudfront.net (CloudFront)",
            "Accept-Language": "en-US,en;q=0.8",
            "CloudFront-Is-Desktop-Viewer": "true",
            "CloudFront-Is-SmartTV-Viewer": "false",
            "CloudFront-Is-Mobile-Viewer": "false",
            "X-Forwarded-For": "127.0.0.1, 127.0.0.2",
            "CloudFront-Viewer-Country": "US",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Upgrade-Insecure-Requests": "1",
            "X-Forwarded-Port": "443",
            "Host": "1234567890.execute-api.us-east-1.amazonaws.com",
            "X-Forwarded-Proto": "https",
            "X-Amz-Cf-Id": "aaaaaaaaaae3VYQb9jd-nvCd-de396Uhbp027Y2JvkCPNLmGJHqlaA==",
            "CloudFront-Is-Tablet-Viewer": "false",
            "Cache-Control": "max-age=0",
            "User-Agent": "Custom User Agent String",
            "CloudFront-Forwarded-Proto": "https",
            "Accept-Encoding": "gzip, deflate, sdch",
        },
        "pathParameters": {"proxy": "/examplepath"},
        "httpMethod": "POST",
        "stageVariables": {"baz": "qux"},
        "path": "/examplepath",
    }


def test_parse_env_list():
    '''Test parsing TagList environment variable'''

    # assert expected tag list
    parsed_tag_list = cost_rules.app._parse_env_list(tag_list_string)
    assert parsed_tag_list == expected_tag_list


def test_account_codes():
    '''Test getting account code mapping from account tags'''
    # stub organizations client
    org = boto3.client('organizations')
    cost_rules.app.org_client = org
    with Stubber(org) as _stub:
            # inject mock account response
            _stub.add_response('list_accounts', mock_account_list)

            # inject a mock tags response for each mock account

            # we are using two codes for three accounts to ensure
            # that accounts are properly grouped under the code
            # found in their respective tags
            _stub.add_response('list_tags_for_resource', mock_resource_tags_a)
            _stub.add_response('list_tags_for_resource', mock_resource_tags_other)
            _stub.add_response('list_tags_for_resource', mock_resource_tags_b)

            # assert codes were collected
            found_account_codes = cost_rules.app.collect_account_tag_codes(expected_tag_list)
            assert found_account_codes == expected_account_codes


def _test_handler_with_env(requests_mock, mocker, event, code, body=None, error=None):
    '''Keep lambda_handler tests DRY'''


def test_lambda_handler(apigw_event, requests_mock, mocker):
    # mock environment variables
    env_vars = {
        'ChartOfAccountsURL': chart_url,
        'CostCenterTagList': tag_list_string,
    }
    mocker.patch.dict(os.environ, env_vars)

    # mock out collect_account_tag_codes() with mock account tags
    mocker.patch('cost_rules.app.collect_account_tag_codes',
                 autospec=True,
                 return_value=expected_account_codes)

    # mock out build_rules() with mock rules
    mocker.patch('cost_rules.app.build_rules',
                 autospec=True,
                 return_value=expected_rules)

    # mock out requests call to get chart of accounts
    response_mock = requests_mock.get(chart_url, json=mock_chart_json)

    # test event
    ret = cost_rules.app.lambda_handler(apigw_event, None)

    assert ret["body"] == json.dumps(expected_rules)
    assert ret['statusCode'] == 200


def test_lambda_handler_err(apigw_event, requests_mock, mocker):
    # mock environment variables
    env_vars = {
        'ChartOfAccountsURL': chart_url,
        'CostCenterTagList': tag_list_string,
    }
    mocker.patch.dict(os.environ, env_vars)

    # mock out collect_account_tag_codes() with mock account tags
    mocker.patch('cost_rules.app.collect_account_tag_codes',
                 autospec=True,
                 side_effect=Exception("Mock Exception"))

    # mock out requests call to get chart of accounts
    response_mock = requests_mock.get(chart_url, json=mock_chart_json)

    # test event
    ret = cost_rules.app.lambda_handler(apigw_event, None)

    assert ret["body"] == "Mock Exception"
    assert ret['statusCode'] == 500