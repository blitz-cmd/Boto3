from types import prepare_class
import boto3
import random

def createbucket():
    s3=boto3.client('s3')
    bname=input("Enter bucket name:")
    bname=bname+"-"+str(random.randint(10000,100000))
    s3.create_bucket(Bucket=bname)

def listbucket():
    s3=boto3.client('s3')
    response=s3.list_buckets()
    buckets = [bucket['Name'] for bucket in response['Buckets']]
    for i in range(len(buckets)):
        print("{}] {}".format(i+1,buckets[i]))

def deletebucket():
    pass

a=0
while(a!=4):
    print()
    print("S3 control panel:")
    print("1)Create bucket")
    print("2)Delete bucket")
    print("3)List bucket")
    print("4)Quit")
    a=int(input("Input option:"))
    print()
    if a==1:
        createbucket()
    elif a==2:
        deletebucket()
    elif a==3:
        listbucket()

