import logging
import re

import boto3

LOG = logging.getLogger(__name__)
LOG.setLevel(logging.INFO)

# This is global so that it can be stubbed in test.
# Because this is global its value will be retained
# in the lambda environment and re-used on warm runs.
org_client = None


def collect_account_tags(tag_names, regex=None):
    """
    Query account tags for fallback program codes if the resource is untagged.
    """

    account_tags = {}

    # create boto client
    global org_client
    if org_client is None:
        org_client = boto3.client("organizations")

    # get list of accounts
    account_pages = org_client.get_paginator("list_accounts").paginate()

    # check for tags on each account
    for account_page in account_pages:
        for account in account_page["Accounts"]:
            account_id = account["Id"]

            tag_pager = org_client.get_paginator("list_tags_for_resource")
            tag_pages = tag_pager.paginate(ResourceId=account_id)

            found = None
            for tag_page in tag_pages:
                for tag in tag_page["Tags"]:
                    if tag["Key"] in tag_names:
                        if regex is not None:
                            # match a regex against the tag
                            found = re.search(regex, tag["Value"])

                            if found is None:
                                LOG.warning(
                                    f'Tag value "{tag["Value"]}" does not match regex "{regex}"'
                                )
                                continue

                            value = found.group(0)
                        else:
                            value = tag["Value"]

                        if value in account_tags:
                            account_tags[value].append(account_id)
                        else:
                            account_tags[value] = [
                                account_id,
                            ]

                        # stop processing tags for this page
                        break

                if found is not None:
                    # stop processing tag pages for this account
                    break

    return account_tags
