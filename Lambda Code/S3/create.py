# Boto3 code to create an s3 bucket

import json
import boto3
from botocore.exceptions import ClientError
import random


def lambda_handler(event, context):
    try:
        s3 = boto3.client('s3', region_name="us-east-1")
        bname = 'whizlabs'
        bname = bname+"-"+str(random.randint(10000, 100000))
        result = s3.create_bucket(Bucket=bname)
        return result
    except ClientError as error:
        raise error
