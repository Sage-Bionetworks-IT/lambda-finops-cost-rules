import json
import logging
import os
import re

import boto3
import requests


LOG = logging.getLogger(__name__)
LOG.setLevel(logging.INFO)

# This is global so that it can be stubbed in test.
# Because this is global its value will be retained
# in the lambda environment and re-used on warm runs.
org_client = None


def _get_os_var(varnam):
    try:
        return os.environ[varnam]
    except KeyError as exc:
        raise Exception(f"The environment variable '{varnam}' must be set")


def _parse_env_list(string):
    '''
    Unpack a CSV into a list of strings.

    In order to pass a list of strings through an environment variable,
    it needs to be encoded in a single string, use CSV.
    '''
    return string.split(',')


def _strip_special_chars(value):
    '''
    The name of a cost category must adhere to: ^(?! )[\p{L}\p{N}\p{Z}-_]*(?<! )$

    Replace any disallowed characters with '_'
    '''
    return re.sub('[^a-zA-Z0-9 -]', '_', value)


def collect_account_tag_codes(tag_names):
    '''
    Query account tags for fallback values if the resource is untagged.
    '''

    account_codes = {}

    # create boto client
    global org_client
    if org_client is None:
        org_client = boto3.client('organizations')

    # get list of accounts
    account_pages = org_client.get_paginator('list_accounts').paginate()

    # check for tags on each account
    for account_page in account_pages:
        for account in account_page['Accounts']:
            account_id = account['Id']

            tag_pager = org_client.get_paginator('list_tags_for_resource')
            tag_pages = tag_pager.paginate(ResourceId=account_id)

            found = None
            for tag_page in tag_pages:
                for tag in tag_page['Tags']:
                    if tag['Key'] in tag_names:
                        # get a 6-digit numeric code from the tag
                        found = re.search(r'[0-9]{6}', tag['Value'])

                        if found is None:
                            LOG.warning(f"No numeric code found in tag: {tag['Value']}")
                            continue

                        code = found.group(0)

                        if code in account_codes:
                            account_codes[code].append(account_id)
                        else:
                            account_codes[code] = [ account_id, ]

                        # stop processing tags for this page
                        break

                if found is not None:
                    # stop processing tag pages for this account
                    break

    return account_codes

def _build_tag_rules(rule_name, tag_names, code):
    results = [
        {
            'Type': 'REGULAR',
            'Value': rule_name,
            'Rule': {
                'Tags': {
                    'Key': tag,
                    'Values': [ code, ],
                    'MatchOptions': [ 'STARTS_WITH', 'ENDS_WITH', ],
                }
            }
        }
        for tag in tag_names
    ]

    return results

def _build_account_rule(rule_name, tag_names, account_ids):
    '''
    Build rule for falling back to account tag if no resource tag is found
    '''

    _and_accounts = {
        'Dimensions': {
            'Key': 'LINKED_ACCOUNT',
            'Values': account_ids,
            'MatchOptions': [ 'EQUALS', ],
        }
    }

    _and_tags = [
        {
            'Tags': {
                'Key': tag,
                'MatchOptions': [ 'ABSENT', ],
            }
        }
        for tag in tag_names
    ]

    _and = []
    _and.append(_and_accounts)
    _and.extend(_and_tags)

    result = {
        'Type': 'REGULAR',
        'Value': rule_name,
        'Rule': {
            'And': _and
        }
    }

    return result


def _build_inherit_rules(tag_names):
    '''
    Build rules for inheriting the category name from a resource tag if no matching code was found
    '''

    results = [
        {
            'Type': 'INHERITED_VALUE',
            'InheritedValue': {
                'DimensionName': 'TAG',
                'DimensionValue': tag,
            }
        }
        for tag in tag_names
    ]

    return results


def build_rules(chart_codes, tag_names, account_codes):
    '''
    Build a list of cost-category rules.
    Rule order matters, first rule matched wins.

    For each program code in our chart of accounts, create rules that:
      1. Check resource tags for the program code.
      2. Check for accounts tagged with the program code.
    Finally, if an unmatched tag value exists, create a new category from it.

    '''
    rules = []

    # first, generate rules for each program code
    for code, name in chart_codes.items():
        safe_name = _strip_special_chars(name)

        if safe_name != name:
            LOG.info(f'{name} renamed to {safe_name}')

        title = f"{code} {safe_name}"

        # generate rules checking each tag
        rules.extend(_build_tag_rules(
            title,
            tag_names,
            code
        ))

        if code in account_codes:
            # if any accounts are tagged with this code,
            # add a rule for them here
            rules.append(_build_account_rule(
                title,
                tag_names,
                account_codes[code]
            ))

    # finally, inherit tag values if no other rule matched
    rules.extend(_build_inherit_rules(tag_names))

    return rules


def lambda_handler(event, context):
    """Sample pure Lambda function

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """

    result = { "statusCode": 200 }
    try:
        # get environment variables
        chart_url = _get_os_var('ChartOfAccountsURL')

        _tag_list = _get_os_var('CostCenterTagList')
        tag_list = _parse_env_list(_tag_list)

        # get account tags
        account_codes = collect_account_tag_codes(tag_list)

        # get chart of accounts
        chart_json = requests.get(chart_url)
        chart_json.raise_for_status()
        chart_data = chart_json.json()

        # generate rules
        rules_data = build_rules(chart_data, tag_list, account_codes)

        # return as json string
        result["body"] = json.dumps(rules_data)
        result["headers"] = { "content-type": "application/json; charset=utf-8" }

    except Exception as exc:
        result["statusCode"] = 500
        result["body"] = str(exc)

    return result
