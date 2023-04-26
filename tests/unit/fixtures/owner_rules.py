# expected set of owner rules built from expected_account_owners
expected_owner_rules = [
    {
        'InheritedValue': {
            'DimensionName': 'TAG',
            'DimensionKey': 'TagOne'
        },
        'Type': 'INHERITED_VALUE'
    },
    {
        'InheritedValue': {
            'DimensionName': 'TAG',
            'DimensionKey': 'TagTwo'
        },
        'Type': 'INHERITED_VALUE'
    },
    {
        'Rule': {
            'Dimensions': {
                'Key': 'LINKED_ACCOUNT',
                'MatchOptions': ['EQUALS'],
                'Values': ['111222333444', '333444555666']
            }
        },
         'Type': 'REGULAR',
        'Value': 'foo@sagebase.org'
    },
    {
        'Rule': {
            'Dimensions': {
                'Key': 'LINKED_ACCOUNT',
                'MatchOptions': ['EQUALS'],
                'Values': ['222333444555']
            }
        },
        'Type': 'REGULAR',
        'Value': 'bar@sagebase.org'
    },
]
