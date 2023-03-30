# mock return for list_tags_for_resource()
mock_resource_owner_tags_foo1 = {
    'Tags': [
        {
            'Key': 'TagOne',
            'Value': "foo@sagebase.org",
        },
    ]
}

# mock return for list_tags_for_resource()
mock_resource_owner_tags_foo2 = {
    'Tags': [
        {
            'Key': 'TagTwo',
            'Value': "foo@sagebase.org",
        },
    ]
}

# mock return for list_tags_for_resource()
mock_resource_owner_tags_bar = {
    'Tags': [
        {
            'Key': 'TagOne',
            'Value': "bar@sagebase.org",
        },
    ]
}

# expected account owner dictionary
expected_account_owners = {
    'foo@sagebase.org': [
        '111222333444',
        '333444555666',
    ],
    'bar@sagebase.org': [
        '222333444555',
    ],
}
