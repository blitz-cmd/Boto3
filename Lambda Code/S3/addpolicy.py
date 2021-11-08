# Boto3 code to add a bucket policy

import json
import boto3
from botocore.exceptions import ClientError
s3_client = boto3.client('s3')
s3_resource = boto3.resource('s3')


def lambda_handler(event, context):
    try:
        bucketname = 'whizlabs-53210'
        key = 'deep.json'
        s3_resource.ObjectAcl(bucketname, key).put(ACL='public-read')
        policy = {
            "Id": "Policy1634014557619",
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "Stmt1634014555554",
                    "Action": [
                        "s3:GetObject"
                    ],
                    "Effect": "Allow",
                    "Resource": "arn:aws:s3:::whizlabs-53210/deep.json",
                    "Principal": "*"
                }
            ]
        }
        policy = json.dumps(policy)
        result = s3_client.put_bucket_policy(Bucket=bucketname, Policy=policy)
        return result
    except ClientError as error:
        raise error
