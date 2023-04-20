mock_category = 'Category Name'

mock_tag_value = 'Value'

mock_account_ids = [
    '111222333444',
    '222333444555'
]

expected_account_rule = {
    'Rule': {
        'Dimensions': {
            'Key': 'LINKED_ACCOUNT',
            'MatchOptions': ['EQUALS'],
            'Values': ['111222333444', '222333444555']
        }
    },
    'Type': 'REGULAR',
    'Value': 'Category Name',
}

expected_tag_rules = [
    {
        'Rule': {
            'Tags': {
                'Key': 'TagOne',
                'MatchOptions': ['STARTS_WITH', 'ENDS_WITH'],
                'Values': ['Value']
            }
        },
       'Type': 'REGULAR',
       'Value': 'Category Name'
    },
    {
        'Rule': {
            'Tags': {
                'Key': 'TagTwo',
                'MatchOptions': ['STARTS_WITH', 'ENDS_WITH'],
                'Values': ['Value']
            }
        },
       'Type': 'REGULAR',
       'Value': 'Category Name'
    },
]

expected_inherit_rules = [
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
