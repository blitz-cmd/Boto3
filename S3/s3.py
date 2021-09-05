import boto3
import random
import string
from botocore.exceptions import ClientError

# bucket_name="boto3-"+''.join(random.choices(string.ascii_lowercase+string.digits,k=10))

#create a bucket
# s3.create_bucket(Bucket=bucket_name,CreateBucketConfiguration={
#     'LocationConstraint':'ap-south-1'
# })

def createbucket(region=None):
    s3=boto3.client('s3')
    bucket_name="boto3-"+''.join(random.choices(string.ascii_lowercase+string.digits,k=10))    
    try:
        if region is None:
            s3.create_bucket(Bucket=bucket_name)
            response=s3.get_bucket_location(Bucket=bucket_name)
            print("Bucket created successfully - {} in region {}".format(bucket_name,response['LocationConstraint']))
        else:
            s3.create_bucket(Bucket=bucket_name,CreateBucketConfiguration={
                'LocationConstraint':region
                })
            response=s3.get_bucket_location(Bucket=bucket_name)
            print("Bucket created successfully - {} in region {}".format(bucket_name,response['LocationConstraint']))

    except ClientError as e:
        print(e)
createbucket(region="ap-south-1")

# #print all bucket names
# for bucket in s3.buckets.all():
#     print(bucket.name)

#upload new file
# data=open('a.txt','rb')
# s3.Bucket('kops-504').put_object(Key='a.txt',Body=data)

