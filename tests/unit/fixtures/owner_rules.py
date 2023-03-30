# expected set of owner rules built from expected_account_owners
expected_owner_rules = [
    {
        'InheritedValue': {
            'DimensionName': 'TAG',
            'DimensionValue': 'TagOne'
        },
        'Type': 'INHERITED_VALUE'
    },
    {
        'InheritedValue': {
            'DimensionName': 'TAG',
            'DimensionValue': 'TagTwo'
        },
        'Type': 'INHERITED_VALUE'
    },
    {
        'Rule': {
            'And': [
                {
                    'Dimensions': {
                        'Key': 'LINKED_ACCOUNT',
                        'MatchOptions': ['EQUALS'],
                        'Values': ['111222333444', '333444555666']
                    }
                },
                {
                    'Tags': {
                        'Key': 'TagOne',
                        'MatchOptions': ['ABSENT']
                    }
                },
                {
                    'Tags': {
                        'Key': 'TagTwo',
                        'MatchOptions': ['ABSENT']
                    }
                }
            ]
        },
         'Type': 'REGULAR',
        'Value': 'foo@sagebase.org'
    },
    {
        'Rule': {
            'And': [
                {
                    'Dimensions': {
                        'Key': 'LINKED_ACCOUNT',
                        'MatchOptions': ['EQUALS'],
                        'Values': ['222333444555']
                    }
                },
                {
                    'Tags': {
                        'Key': 'TagOne',
                        'MatchOptions': ['ABSENT']
                    }
                },
                   {
                    'Tags': {
                        'Key': 'TagTwo',
                        'MatchOptions': ['ABSENT']
                    }
                }
            ]
        },
        'Type': 'REGULAR',
        'Value': 'bar@sagebase.org'
    },
]
