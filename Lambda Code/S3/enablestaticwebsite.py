# Boto3 code to enable static website

import json
import boto3
from botocore.exceptions import ClientError
s3 = boto3.client('s3')


def lambda_handler(event, context):
    try:
        static_website_configuration = {
            'ErrorDocument': {'Key': 'error.html'},
            'IndexDocument': {'Suffix': 'index.html'},
        }
        result = s3.put_bucket_website(
            Bucket='whizlabs53210', WebsiteConfiguration=static_website_configuration)
        return result
    except ClientError as error:
        raise error
