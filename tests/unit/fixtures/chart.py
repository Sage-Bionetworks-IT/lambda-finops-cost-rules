# injected env var value
chart_url = "https://example.com/path"

# mock chart of accounts returned from `lambda-mips-api`
mock_chart_json = """{
"000000": "No Program",
"000001": "Other",
"123456": "Program Part A",
"654321": "Other Program"
}"""

# expected parsed chart of accounts
expected_chart_dict = {
    "000000": "No Program",
    "000001": "Other",
    "123456": "Program Part A",
    "654321": "Other Program",
}
