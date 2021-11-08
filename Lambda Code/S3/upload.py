# Boto3 code to create json object and upload to S3

import json
import boto3
from botocore.exceptions import ClientError
s3 = boto3.client('s3')


def lambda_handler(event, context):
    try:
        bucketname = 'whizlabs-53210'
        file = {}
        file['id'] = '1'
        file['name'] = 'deep'
        filename = 'deep'+'.json'
        upload = bytes(json.dumps(file).encode('UTF-8'))
        result = s3.put_object(Bucket=bucketname, Key=filename, Body=upload)
        return result
    except ClientError as error:
        raise error
