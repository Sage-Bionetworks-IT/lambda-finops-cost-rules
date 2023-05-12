from cost_rules import builder, chart_client, s3_client, tag_client, util

import json
import logging


LOG = logging.getLogger(__name__)
LOG.setLevel(logging.INFO)


def _build_program_rules(chart_codes, tag_names, account_codes):
    '''
    Build a list of cost-category rules.
    Rule order matters, first rule matched wins.

    For each program code in our chart of accounts, create rules that:
      1. Check resource tags for the program code.
      2. Check for accounts tagged with the program code.
    Finally, if an unmatched tag value exists, create a new category from it.

    '''
    rules = []
    account_rules = []

    # first, generate rules for each program code
    for code, name in chart_codes.items():
        safe_name = util.safe_category_name(name)

        if safe_name != name:
            LOG.info(f'{name} renamed to {safe_name}')

        title = f"{code} {safe_name}"

        # generate rules checking each tag
        rules.extend(builder.build_tag_rules(
            title,
            tag_names,
            code
        ))

        if code in account_codes:
            # if any accounts are tagged with this code,
            # add an account rule for them here
            account_rules.append(builder.build_account_rule(
                title,
                tag_names,
                account_codes[code]
            ))

    # ensure that account rules come after resource rules
    rules.extend(account_rules)

    # finally, inherit tag values if no other rule matched
    rules.extend(builder.build_inherit_rules(tag_names))

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

    result = { "statusCode": 201 }
    try:
        # get environment variables
        chart_url = util.get_os_var('ChartOfAccountsURL')

        _tag_list = util.get_os_var('ProgramCodeTagList')
        tag_list = util.parse_env_list(_tag_list)

        # get account tags
        account_codes = tag_client.collect_account_tags(tag_list, r'[0-9]{6}')

        # get chart of accounts
        chart_data = chart_client.collect_chart_of_accounts(chart_url)

        # generate rules
        rules_data = _build_program_rules(chart_data, tag_list, account_codes)

        # write rules to s3
        s3_client.write_rules_to_s3('cost-categories/program-code-rules.yaml', json.dumps(rules_data))

    except Exception as exc:
        result["statusCode"] = 500
        result["body"] = str(exc)

    return result
