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
    listbucket()
    print()
    bucketname=input("Enter bucket name:")
    print()
    b=0
    while(b!=6):
        print("1)List all objects in bucket")
        print("2)Empty the bucket")
        print("3)Delete particular object in bucket")
        print("4)Delete bucket policy")
        print("5)Delete bucket")
        print("6)Quit")
        b=int(input("Choose option:"))
        print()
        s3=boto3.client('s3')
        if b==1:            
            list=s3.list_objects(Bucket=bucketname)["Contents"]            
            print("Bucket contents are:")
            for obj in list:
                print(obj["Key"])
            print()
        elif b==2:
            list=s3.list_objects(Bucket=bucketname)["Contents"]
            print("Deleting all objects in {}".format(bucketname))
            for obj in list:
                print("Deleting - {}".format(obj["Key"]))
                s3.delete_object(Bucket=bucketname,Key=obj["Key"])
            print()
        elif b==3:
            list=s3.list_objects(Bucket=bucketname)["Contents"]
            print("Deleting only one object in {}".format(bucketname))
            for obj in list:
                print(obj["Key"])
            s3.delete_object(Bucket=bucketname,Key=input("Enter object name to be deleted:"))
            print("Object deleted successfully")
            print()
        elif b==4:
            s3.delete_bucket_policy(Bucket=bucketname)
            print("{} bucket policy deleted successfully".format(bucketname))
            print()
        elif b==5:
            s3.delete_bucket(Bucket=bucketname)
            print("{} bucket deleted successfully".format(bucketname))
            print()
            break

def uploadobject():
    s3=boto3.client('s3')
    listbucket()
    print()
    bucketname=input("Enter bucket name:")
    print("Filename should include extension also and should be present in current working directory")
    filename=input("Name of the file to be uploaded:")
    s3.upload_file(Filename=filename,Bucket=bucketname,Key=filename)

a=0
while(a!=5):
    print()
    print("S3 control panel:")
    print("1)Create bucket")
    print("2)List bucket")
    print("3)Upload files in bucket")
    print("4)Delete bucket")
    print("5)Quit")
    a=int(input("Choose option:"))
    print()
    if a==1:
        createbucket()
    elif a==2:
        listbucket()
    elif a==3:
        uploadobject()
    elif a==4:
        deletebucket()
        