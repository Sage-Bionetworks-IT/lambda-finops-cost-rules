from cost_rules import builder, chart_client, tag_client, util

import json


def _build_owner_rules(tag_names, account_owners):
    '''
    Build a list of cost-category rules.

    First, inherit any tag values in their listed order.
    Then fall back to any account tags for untagged resources.
    '''

    rules = []

    # Inherit tag values
    rules.extend(builder.build_inherit_rules(tag_names))

    # Fall back on account tag values
    for owner in account_owners:
        rules.append(builder.build_account_rule(
            owner,
            tag_names,
            account_owners[owner]
        ))

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
        _tag_list = util.get_os_var('OwnerEmailTagList')
        tag_list = util.parse_env_list(_tag_list)

        # get account tags
        account_owners = tag_client.collect_account_tags(tag_list)

        # generate rules
        rules_data = _build_owner_rules(tag_list, account_owners)

        result["body"] = json.dumps(rules_data)
        result["headers"] = { "content-type": "application/json; charset=utf-8" }

    except Exception as exc:
        result["statusCode"] = 500
        result["body"] = str(exc)

    return result
