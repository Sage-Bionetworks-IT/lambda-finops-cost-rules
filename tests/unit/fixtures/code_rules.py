# expected set of program rules built from expected_chart_dict and expected_account_codes
expected_program_rules = [
    {
        "Rule": {
             "Tags": {
                 "Key": "TagOne",
                 "MatchOptions": [ "STARTS_WITH", "ENDS_WITH" ],
                 "Values": [ "000000" ],
             }
        },
        "Type": "REGULAR",
        "Value": "000000 No Program",
    },
    {
        "Rule": {
             "Tags": {
                 "Key": "TagTwo",
                 "MatchOptions": [ "STARTS_WITH", "ENDS_WITH" ],
                 "Values": [ "000000" ],
             }
        },
        "Type": "REGULAR",
        "Value": "000000 No Program",
    },
    {
        "Rule": {
             "Tags": {
                 "Key": "TagOne",
                 "MatchOptions": [ "STARTS_WITH", "ENDS_WITH" ],
                 "Values": [ "000001" ],
             }
        },
        "Type": "REGULAR",
        "Value": "000001 Other",
    },
    {
        "Rule": {
             "Tags": {
                 "Key": "TagTwo",
                 "MatchOptions": [ "STARTS_WITH", "ENDS_WITH" ],
                 "Values": [ "000001" ],
             }
        },
        "Type": "REGULAR",
        "Value": "000001 Other",
    },
    {
        "Rule": {
             "Tags": {
                 "Key": "TagOne",
                 "MatchOptions": [ "STARTS_WITH", "ENDS_WITH" ],
                 "Values": [ "123456" ],
             }
        },
        "Type": "REGULAR",
        "Value": "123456 Program Part A",
    },
    {
        "Rule": {
             "Tags": {
                 "Key": "TagTwo",
                 "MatchOptions": [ "STARTS_WITH", "ENDS_WITH" ],
                 "Values": [ "123456" ],
             }
        },
        "Type": "REGULAR",
        "Value": "123456 Program Part A",
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
        'Value': '123456 Program Part A'
    },
    {
        "Rule": {
             "Tags": {
                 "Key": "TagOne",
                 "MatchOptions": [ "STARTS_WITH", "ENDS_WITH" ],
                 "Values": [ "654321" ],
             }
        },
        "Type": "REGULAR",
        "Value": "654321 Other Program",
    },
    {
        "Rule": {
             "Tags": {
                 "Key": "TagTwo",
                 "MatchOptions": [ "STARTS_WITH", "ENDS_WITH" ],
                 "Values": [ "654321" ],
             }
        },
        "Type": "REGULAR",
        "Value": "654321 Other Program",
    },
    {
        'Rule': {
            'And': [
                {
                    'Dimensions': {
                        'Key': 'LINKED_ACCOUNT',
                        'MatchOptions': ['EQUALS'],
                        'Values': ['222333444555', ]
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
        "Value": "654321 Other Program",
    },
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
]
