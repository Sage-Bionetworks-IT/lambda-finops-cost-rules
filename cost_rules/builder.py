def build_tag_rules(rule_name, tag_names, code):
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

def build_account_rule(rule_name, tag_names, account_ids):
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


def build_inherit_rules(tag_names):
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
