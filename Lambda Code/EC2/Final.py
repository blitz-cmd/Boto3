import json
import boto3
from botocore.exceptions import ClientError
import urllib3
region = 'us-east-1'

def lambda_handler(event, context):
    try:
        dictionary={}
        service=0
        ec2 = boto3.client('ec2', region_name=region)
        ec2_response = ec2.describe_instances()
        instances_full_details = ec2_response['Reservations']
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
        
        elbv2=boto3.client('elbv2', region_name=region)
        elbv2_response = elbv2.describe_load_balancers()['LoadBalancers']
        res_count=0
        try:
            
            #Checking for elb
            elbv2_response[0]['LoadBalancerArn']
            for elb in elbv2_response:
                dict_count=0
                dict={}
                dict_count+=1
                
                #Spliting id for ELB dns name
                elb_id=elb['DNSName'].split('.')[0]
                dict[str(dict_count)]="Your Application LB Id is :"+elb_id
                dict_count+=1
                
                #Checking for public facing or private lb
                dict[str(dict_count)]="The ELB is "+elb['Scheme']
                dict_count+=1
                
                #Printing dns of elb
                elb_dns=elb['DNSName']
                dict[str(dict_count)]="The ELB DNS is "+elb_dns
                try:
                    
                    #Checking for target group
                    elb_arn=elb['LoadBalancerArn']
                    targetgroup_response=elbv2.describe_target_groups(LoadBalancerArn=elb_arn)['TargetGroups'][0]
                    dict_count+=1
                    tg_arn=targetgroup_response['TargetGroupArn']
                    dict[str(dict_count)]="The target group of ELB is "+tg_arn
                    try:
                        
                        #Checking for any instance attached to the target group
                        targetgrouphealth_response=elbv2.describe_target_health(TargetGroupArn=tg_arn)['TargetHealthDescriptions']
                        # print(targetgrouphealth_response)
                        tg_dict={}
                        tg_count=0
                        try:
                            for tg in targetgrouphealth_response:
                                instance=tg['Target']['Id']
                                tg_count+=1
                                tg_dict[str(tg_count)]="EC2 with id : "+instance
                        except Exception as error:
                            print("No instance found")
                        dict_count+=1
                        dict[str(dict_count)]=tg_dict
                    except Exception as error:
                        print("Error with target group heath")
                    finally:
                        
                        #Printing health and unhealth threshold of elb
                        dict_count+=1
                        dict[str(dict_count)]="Health threshold of ELB is "+str(targetgroup_response['HealthyThresholdCount'])
                        dict_count+=1
                        dict[str(dict_count)]="Unhealth threshold of ELB is "+str(targetgroup_response['UnhealthyThresholdCount'])
                        try:
                            
                            #Accesing elb dns
                            http=urllib3.PoolManager()
                            ip="http://"+elb_dns
                            dns_req=http.request('GET',ip,timeout=1.0)
                            dict_count+=1
                            dict[str(dict_count)]="Able to access the ELB URL"
                        except Exception as error:
                            dict_count+=1
                            dict[str(dict_count)]="Cannot access the ELB URL"
                        res_count+=1
                        qw="ELB-"+str(res_count)
                        dictionary[qw]=dict
                except Exception as error:
                    print("Error with target group")
            result=json.dumps(dictionary)
            return result
            # return dictionary
        except Exception as error:
            print("No loadbalancer found")
    except Exception as error:
        print("Boto3 Assignment Failed")
