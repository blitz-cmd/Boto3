import json
import boto3
from botocore.exceptions import ClientError
import urllib3
region = 'us-east-1'

def lambda_handler(event, context):
    elbv2=boto3.client('elbv2', region_name=region)
    elbv2_response = elbv2.describe_load_balancers()['LoadBalancers']
    res={}
    res_count=0
    try:
        
        #Checking for elb
        elbv2_response[0]['LoadBalancerArn']
        for elb in elbv2_response:
            dict_count=0
            dictionary={}
            dict_count+=1
            
            #Spliting id for ELB dns name
            elb_id=elb['DNSName'].split('.')[0]
            dictionary[str(dict_count)]="Your Application LB Id is :"+elb_id
            dict_count+=1
            
            #Checking for public facing or private lb
            dictionary[str(dict_count)]="The ELB is "+elb['Scheme']
            dict_count+=1
            
            #Printing dns of elb
            elb_dns=elb['DNSName']
            dictionary[str(dict_count)]="The ELB DNS is "+elb_dns
            try:
                
                #Checking for target group
                elb_arn=elb['LoadBalancerArn']
                targetgroup_response=elbv2.describe_target_groups(LoadBalancerArn=elb_arn)['TargetGroups'][0]
                dict_count+=1
                tg_arn=targetgroup_response['TargetGroupArn']
                dictionary[str(dict_count)]="The target group of ELB is "+tg_arn
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
                    dictionary[str(dict_count)]=tg_dict
                except Exception as error:
                    print("Error with target group heath")
                finally:
                    
                    #Printing health and unhealth threshold of elb
                    dict_count+=1
                    dictionary[str(dict_count)]="Health threshold of ELB is "+str(targetgroup_response['HealthyThresholdCount'])
                    dict_count+=1
                    dictionary[str(dict_count)]="Unhealth threshold of ELB is "+str(targetgroup_response['UnhealthyThresholdCount'])
                    try:
                        
                        #Accesing elb dns
                        http=urllib3.PoolManager()
                        ip="http://"+elb_dns
                        dns_req=http.request('GET',ip,timeout=1.0)
                        dict_count+=1
                        dictionary[str(dict_count)]="Able to access the ELB URL"
                    except Exception as error:
                        dict_count+=1
                        dictionary[str(dict_count)]="Cannot access the ELB URL"
                    res_count+=1
                    res[str(res_count)]=dictionary
            except Exception as error:
                print("Error with target group")
        # result=json.dumps(res)
        # return result
        return res
    except Exception as error:
        print("No loadbalancer found")
