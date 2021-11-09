import json
import boto3
from botocore.exceptions import ClientError
import urllib3
region = 'us-east-1'

ec2 = boto3.client('ec2', region_name=region)

def lambda_handler(event, context):
    dictionary={}
    service=0
    response = ec2.describe_instances()
    instances_full_details = response['Reservations']
    for instance_detail in instances_full_details:
        group_instances = instance_detail['Instances']
        for instance in group_instances:
            dict_count=0
            string={}
            try:
                
                #Checking if instance is public or not
                publicIp="The public IP of EC2 is :"+instance['PublicIpAddress']
            except Exception as error:
                publicIp="Instance is private"
            finally:
                
                #Instance id
                dict_count+=1
                string[str(dict_count)]="Your EC2 Instance Id is :"+instance['InstanceId']
                
                #AMI description
                image_id=instance['ImageId']
                di_response=ec2.describe_images(ImageIds=[
                        image_id,
                    ])
                description=di_response['Images'][0]['Description']
                
                #EC2 architecture and ami description
                dict_count+=1
                string[str(dict_count)]="The EC2 Architecture is "+instance['InstanceType']+" and AMI is "+description
                
                #Public ip of EC2
                dict_count+=1
                string[str(dict_count)]=publicIp
                try:
                    
                    #Checking security group
                    sg_dict={}
                    sg=instance['SecurityGroups'][0]['GroupId']
                    securitygroup="The Security group id is "+sg
                    security_group_response=ec2.describe_security_groups(GroupIds=[sg])
                    
                    #Checking for ports of sg
                    port_response=security_group_response['SecurityGroups'][0]['IpPermissions']
                    count=0
                    for i in port_response:
                        count+=1
                        try:
                            cidr_sg=i['UserIdGroupPairs'][0]['GroupId']
                            sg_dict[count]="Port No "+str(i['FromPort'])+" and CIDR "+str(cidr_sg)
                        except Exception as error:
                            sg_dict[count]="Port No "+str(i['FromPort'])+" and CIDR "+str(i['IpRanges'][0]['CidrIp'])
                    
                    #Security group
                    dict_count+=1
                    string[str(dict_count)]=securitygroup
                    
                    #Ports of sg
                    dict_count+=1
                    string[str(dict_count)]="The ports are : "
                    dict_count+=1
                    string[str(dict_count)]=sg_dict
                except Exception as error:
                    securitygroup="No security group present"
                    dict_count+=1
                    string[str(dict_count)]=securitygroup
                finally:
                    
                    #Checking key-pair
                    try:
                        keypair="The key Pair of EC2 instance is :"+instance['KeyName']+".pem"
                    except Exception as error:
                        keypair="No keypair found"
                    finally:
                        dict_count+=1
                        string[str(dict_count)]=keypair
                        try:
                            
                            #Checking apache installation
                            ip="http://"+instance['PublicIpAddress']
                            http = urllib3.PoolManager()
                            request1 = http.request('GET',ip)
                            dict_count+=1
                            string[str(dict_count)]="Installed Apache in the server"
                            try:
                                
                                #Checking test.html is installed or not
                                ip="http://"+instance['PublicIpAddress']+"/test.html"
                                request2=http.request('GET',ip)
                                if request2.status==200:
                                    dict_count+=1
                                    string[str(dict_count)]="Added test.html file in the Server"
                                else:
                                    dict_count+=1
                                    string[str(dict_count)]="test.html not found in the Server"
                            except Exception as error:
                                print(error)
                        except Exception as error:
                            dict_count+=1
                            string[str(dict_count)]="Apache not installed in the server"
                            
                        finally:
                            
                            #Volume id and size
                            volume_id=instance['BlockDeviceMappings'][0]['Ebs']['VolumeId']
                            ec2_resource = boto3.resource('ec2')
                            volume=str(ec2_resource.Volume(volume_id).size)
                            dict_count+=1
                            string[str(dict_count)]="Root Volume Id of EC2 is "+volume_id+" and the volume size is "+volume+" GB"
                            service+=1
                            qw="EC2-"+str(service)
                            dictionary[qw]=string
    result=json.dumps(dictionary)
    return result
    # return dictionary
# print(lambda_handler("event", "context"))