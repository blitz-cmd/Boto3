# Boto3 code to read an object from one bucket and add to another bucket

import json
import boto3
from botocore.exceptions import ClientError
s3_resource = boto3.resource('s3')


def lambda_handler(event, context):
    try:
        copy_source = {
            'Bucket': 'whizlabs-53210',
            'Key': 'deep.json'
        }
        result = s3_resource.meta.client.copy(
            copy_source, 'whizlabs-67612', 'deep_copy.json')
        return result
    except ClientError as error:
        raise error
