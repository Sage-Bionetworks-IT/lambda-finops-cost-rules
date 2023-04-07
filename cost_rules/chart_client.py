import requests
import validators


def collect_chart_of_accounts(chart_url):
    '''
    Query lambda-mips-api for current chart of accounts.
    '''

    # check for valid url
    if not validators.url(chart_url):
        raise Exception(f'Invalid URL: {chart_url}')

    # get chart of accounts
    chart_json = requests.get(chart_url)
    chart_json.raise_for_status()

    # return unpacked json data
    return chart_json.json()
