# Boto3 code to delete an object

import json
import boto3
from botocore.exceptions import ClientError
s3 = boto3.client('s3')


def lambda_handler(event, context):
    try:
        bucketname = 'whizlabs-53210'
        result = s3.delete_object(Bucket=bucketname, Key='iam.png')
        return result
    except ClientError as error:
        raise error
