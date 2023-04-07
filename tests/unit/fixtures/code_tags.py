# mock return for list_tags_for_resource()
mock_resource_code_tags_a = {
    'Tags': [
        {
            'Key': 'TagOne',
            'Value': "Program Part A / 123456",
        },
    ]
}

# mock return for list_tags_for_resource()
mock_resource_code_tags_b = {
    'Tags': [
        {
            'Key': 'TagOne',
            'Value': "Program Part B / 123456",
        },
    ]
}

# mock return for list_tags_for_resource()
mock_resource_code_tags_other = {
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
