import os

from botocore.stub import Stubber

import cost_rules.s3_client
from .fixtures.s3_yaml import *


def test_write_to_s3(mocker, s3_client):
    """
    Test getting account code mapping from account tags
    """
    # stub organizations client
    cost_rules.s3_client.s3_client = s3_client
    with Stubber(s3_client) as _stub:
        # mock environment variables
        env_vars = {
            "BucketName": "TestBucket",
        }
        mocker.patch.dict(os.environ, env_vars)

        expected_params = {
            "Bucket": "TestBucket",
            "Key": "file.yaml",
            "Body": expected_yaml_str,
        }

        # inject mock account response
        _stub.add_response("put_object", {}, expected_params)

        # assert no exception
        cost_rules.s3_client.write_rules_to_s3("file.yaml", mock_json_rules)

        _stub.assert_no_pending_responses()
