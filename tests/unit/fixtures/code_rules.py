# expected set of program rules built from expected_chart_dict and expected_account_codes
expected_program_rules = [
    {
        "Rule": {
            "Tags": {
                "Key": "TagOne",
                "MatchOptions": ["ENDS_WITH"],
                "Values": ["000000"],
            }
        },
        "Type": "REGULAR",
        "Value": "000000 No Program",
    },
    {
        "Rule": {
            "Tags": {
                "Key": "TagTwo",
                "MatchOptions": ["ENDS_WITH"],
                "Values": ["000000"],
            }
        },
        "Type": "REGULAR",
        "Value": "000000 No Program",
    },
    {
        "Rule": {
            "Tags": {
                "Key": "TagOne",
                "MatchOptions": ["ENDS_WITH"],
                "Values": ["000001"],
            }
        },
        "Type": "REGULAR",
        "Value": "000001 Other",
    },
    {
        "Rule": {
            "Tags": {
                "Key": "TagTwo",
                "MatchOptions": ["ENDS_WITH"],
                "Values": ["000001"],
            }
        },
        "Type": "REGULAR",
        "Value": "000001 Other",
    },
    {
        "Rule": {
            "Tags": {
                "Key": "TagOne",
                "MatchOptions": ["ENDS_WITH"],
                "Values": ["123456"],
            }
        },
        "Type": "REGULAR",
        "Value": "123456 Program Part A",
    },
    {
        "Rule": {
            "Tags": {
                "Key": "TagTwo",
                "MatchOptions": ["ENDS_WITH"],
                "Values": ["123456"],
            }
        },
        "Type": "REGULAR",
        "Value": "123456 Program Part A",
    },
    {
        "Rule": {
            "Tags": {
                "Key": "TagOne",
                "MatchOptions": ["ENDS_WITH"],
                "Values": ["654321"],
            }
        },
        "Type": "REGULAR",
        "Value": "654321 Other Program",
    },
    {
        "Rule": {
            "Tags": {
                "Key": "TagTwo",
                "MatchOptions": ["ENDS_WITH"],
                "Values": ["654321"],
            }
        },
        "Type": "REGULAR",
        "Value": "654321 Other Program",
    },
    {
        "Rule": {
            "Dimensions": {
                "Key": "LINKED_ACCOUNT",
                "MatchOptions": ["EQUALS"],
                "Values": ["111222333444", "333444555666"],
            }
        },
        "Type": "REGULAR",
        "Value": "123456 Program Part A",
    },
    {
        "Rule": {
            "Dimensions": {
                "Key": "LINKED_ACCOUNT",
                "MatchOptions": ["EQUALS"],
                "Values": [
                    "222333444555",
                ],
            }
        },
        "Type": "REGULAR",
        "Value": "654321 Other Program",
    },
    {
        "InheritedValue": {"DimensionName": "TAG", "DimensionKey": "TagOne"},
        "Type": "INHERITED_VALUE",
    },
    {
        "InheritedValue": {"DimensionName": "TAG", "DimensionKey": "TagTwo"},
        "Type": "INHERITED_VALUE",
    },
]
