import logging

import boto3
import yaml

from cost_rules import util

LOG = logging.getLogger(__name__)
LOG.setLevel(logging.INFO)

# This is global so that it can be stubbed in test.
# Because this is global its value will be retained
# in the lambda environment and re-used on warm runs.
s3_client = None


def put_s3_object(bucket, key, body):
    """
    Write file data to S3
    """

    global s3_client
    if s3_client is None:
        s3_client = boto3.client("s3")

    s3_client.put_object(Bucket=bucket, Key=key, Body=body)


def write_rules_to_s3(filename, rules_json):
    """
    Build YAML object encapsulating our JSON object
    """

    bucket = util.get_os_var("BucketName")

    yaml_obj = {}
    yaml_obj["Rules"] = rules_json
    yaml_str = yaml.dump(yaml_obj)

    put_s3_object(bucket, filename, yaml_str)
