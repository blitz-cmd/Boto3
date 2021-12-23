#Python code to detect DAX and EC2 

import json
import boto3
import re

def lambda_handler(event, context):
    aws_access_key_id=event['aws_access_key_id']
    aws_secret_access_key=event['aws_secret_access_key']
    
    #Final return variable
    #return variable
    test_result = {}
    #status
    
    dax_status_flag = []
    ec2_status_flag = []
    
    #user-info
    user_info = {}
    
    #task_status
    task_status1 = {}
    task_status2 = {}
    dax_task_status = {}
    ec2_task_status = {}
    total_task_status = {}
    
    #final_result
    finalresult = {}
    # final_strin1g ={}
    dax_finalresult = {}
    ec2_finalresult = {}
    complete_details = {}
    custer_array = []
     
    
    try:
        ec2Client = boto3.client('ec2', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name='us-east-1')
        daxClient = boto3.client('dax', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name='us-east-1')
        list_ec2_flag = True
        list_dax_flag = True
        
        #List Number of dax cluster
        try:
            dax_cluster = daxClient.describe_clusters()
            no_of_dax_cluster = len(dax_cluster['Clusters'])
            if no_of_dax_cluster > 0:
                user_info["1"] = "You have created {} DynamoDB DAX Cluster in this lab.".format(no_of_dax_cluster)
            else:
                user_info["1"] = "You have created 0 DynamoDB DAX Cluster in this lab."
                task_status1["Create DynamoDB DAX Cluster status"] ="failed"
                task_status1["Select 3 nodes status"] = "failed"
                task_status1["Select node type as dax.t2.small status"] = "failed"
                task_status1["DAX Cluster current status as available"] = "failed"
                task_status1["Select Encrption enable status"] = "failed"
                dax_task_status["Cluster"] = task_status1
                dax_finalresult["Cluster"] = "You have not created any DynamoDB DAX Cluster."
                list_dax_flag = False
            
        except Exception as e:
            print("listing number of DAX Cluster failed because:",e)
            
        #list number of ec2 instance
        try:
            ec2_instance=ec2Client.describe_instances()
            no_of_ec2_instance=len(ec2_instance['Reservations'])
            if no_of_ec2_instance > 0:
                user_info["2"] = "You have created {} EC2 Instance in this lab.".format(no_of_ec2_instance)
            else:
                user_info["2"] = "You have created 0 EC2 Instance in this lab."
                task_status2["Create EC2 Instance status"] = "failed"
                task_status2["Select Amazon Linux 2 AMI status"] = "failed"
                task_status2["Select IAM role for EC2 status"] = "failed"
                task_status2["Enable SSH port in security group status"] = "failed"
                task_status2["Creation of keypair for EC2 Instance status"] = "failed"
                ec2_task_status["Instance"] = task_status2
                ec2_finalresult["Instance"] = "You have not created any EC2 Instance."
                list_ec2_flag = False
            
        except Exception as e:
            print("listing number of EC2 Cluster failed because:",e)
        
        total_task_status["DynamoDB DAX"] = dax_task_status
        total_task_status["EC2 Instance"] = ec2_task_status
        complete_details["DynamoDB DAX"] = dax_finalresult
        complete_details["EC2 Instance"] = ec2_finalresult
        if list_dax_flag == False and list_ec2_flag == False:
            test_result["lab-validation-status"] = {"status": "failed"}
            test_result["lab-user-info"] = user_info
            test_result["lab-task-status"] = total_task_status
            test_result["lab-usertask-complete-details"] = complete_details
            print(test_result)
            return test_result
            
        #Describing DAX cluster
        if list_dax_flag:
            try:
                dax_cluster_desc = daxClient.describe_clusters()
                count_dax = 1
                for lc in dax_cluster_desc['Clusters']:
                    status = []
                    ClusterName = lc['ClusterName']
                    final_string1 = {}
                    task_status1 = {}
                    task_status1["Create DAX Cluster status"] = "success"
                    status.append("Success")
                    TotalNodes = lc['TotalNodes']
                    NodeType = lc['NodeType']
                    Address = lc['ClusterDiscoveryEndpoint']['Address']
                    Port = lc['ClusterDiscoveryEndpoint']['Port']
                    Status = lc['Status']
                    SubnetGroup = lc['SubnetGroup']
                    SecurityGroupIdentifier = lc['SecurityGroups'][0]['SecurityGroupIdentifier']
                    IamRoleArn = lc['IamRoleArn'].split("/")[2]
                    SSEDescription = lc['SSEDescription']['Status']
                    
                    if TotalNodes == 3:
                        task_status1["Select 3 nodes status"] = "success"
                        status.append("Success")
                    else:
                        task_status1["Select 3 nodes status"] = "failed"
                        status.append("Failed")
                    
                    if NodeType == 'dax.t2.small':
                        task_status1["Select node type as dax.t2.small status"] = "success"
                        status.append("Success")
                    else:
                        task_status1["Select node type as dax.t2.small status"] = "failed"
                        status.append("Failed")  
                        
                    if Status == 'available':
                        task_status1["DAX Cluster current status as available"] = "success"
                        status.append("Success")
                    else:
                        task_status1["DAX Cluster current status as available"] = "failed"
                        status.append("Failed")
                        
                    if SSEDescription == 'ENABLED':
                        task_status1["Select Encrption enable status"] = "success"
                        status.append("Success")
                    else:
                        task_status1["Select Encrption enable status"] = "failed"
                        status.append("Failed")
                        
                    #Check status of service
                    try:
                        if "Failed" in status:
                            dax_status_flag.append("Failed")
                        else:
                            dax_status_flag.append("Success")
                    except Exception as e:
                        print("Status check of DAX Cluster Status failed because ", e)
                    
                    #Creating the final result string
                    try: 
                        j = 1
                        final_string1[j] = "You have created a DAX cluster with name {}.".format(ClusterName)
                        j+=1
                        final_string1[j] = "The total number of nodes is {}.".format(TotalNodes)
                        j+=1
                        final_string1[j] = "The selected node type is {}.".format(NodeType)
                        j+=1
                        final_string1[j] = "The endpoint for the cluster is {} and it is using port number {}.".format(Address, Port)
                        j+=1
                        final_string1[j] = "The current status of the cluster is {}.".format(Status)
                        j+=1
                        final_string1[j] = "The selected subnet group is {}.".format(SubnetGroup)
                        j+=1
                        final_string1[j] = "The selected security group is {}.".format(SecurityGroupIdentifier)
                        j+=1
                        final_string1[j] = "The selected IAM role is {}.".format(IamRoleArn)
                        j+=1
                        final_string1[j] = "Encryption status is {}.".format(SSEDescription)
                        
                        dax_task_status["Cluster:" +str(count_dax)] = task_status1
                        dax_finalresult["Cluster:" +str(count_dax)] = final_string1
                        
                        count_dax += 1
                    except Exception as e:
                        print("Final result string creation failed because: ",e)
                            
            except Exception as e:
                print("Listing dax cluster failed because:",e)
            
            total_task_status["DynamoDB DAX"] = dax_task_status
            complete_details["DynamoDB DAX"] = dax_finalresult
        
        #describe ec2 instance
        if list_ec2_flag:
            try:
                ec2_instance=ec2Client.describe_instances()
                instances_full_details = ec2_instance['Reservations']
                count_ec2 = 1
                for instance_detail in instances_full_details:
                    instance=instance_detail['Instances'][0]
                    task_status2 = {}
                    final_string2 = {}
                    status = []
                    task_status2["Create EC2 Instance status"] = "success"
                    status.append("Success")
                    image_id=instance['ImageId']
                    di_response=ec2Client.describe_images(ImageIds=[image_id,])
                    ami_description=di_response['Images'][0]['Description']
                    
                    #checking status of service
                    if "Amazon" in ami_description:
                        task_status2["Select Amazon Linux 2 AMI status"] = "success"
                        status.append("Success")
                    else:
                        task_status2["Select Amazon Linux 2 AMI status"] = "failed"
                        status.append("Failed")
                    try:
                        iam_policy=instance['IamInstanceProfile']['Arn'].split("/")[1]
                        task_status2["Select IAM role for EC2 status"] = "success"
                        status.append("Success")
                    except Exception as e:
                        task_status2["Select IAM role for EC2 status"] = "failed"
                        status.append("Failed")
                    try:
                        port=[]
                        sg_id=instance['SecurityGroups'][0]['GroupId']
                        security_group_response=ec2Client.describe_security_groups(GroupIds=[sg_id])
                        port_response=security_group_response['SecurityGroups'][0]['IpPermissions']
                        for i in port_response:
                            port.append(str(i['FromPort']))
                        if "22" in port:
                            task_status2["Enable SSH port in security group status"] = "success"
                            status.append("Success")
                        else:
                            task_status2["Enable SSH port in security group status"] = "failed"
                            status.append("Failed")
                    except Exception as e:
                        task_status2["Enable SSH port in security group status"] = "failed"
                        status.append("Failed")
                    try:
                        keypair=instance['KeyName']+".pem"
                        task_status2["Creation of keypair for EC2 Instance status"] = "success"
                        status.append("Success")
                    except Exception as e:
                        task_status2["Creation of keypair for EC2 Instance status"] = "failed"
                        status.append("Failed")
                    try:
                        if "Failed" in status:
                            ec2_status_flag.append("Failed")
                        else:
                            ec2_status_flag.append("Success")
                    except Exception as e:
                        print("Status check of EC2 Instance Status failed because ", e)
                        
                    #Creating the final result string
                    try:
                        j=1
                        final_string2[j] = "You have launched an EC2 Instance with {}.".format(instance['InstanceId'])
                        j+=1
                        final_string2[j] = "You have selected {} and {} as Instance Type.".format(ami_description,instance['InstanceType'])
                        j+=1
                        try:
                            final_string2[j] = "You have selected {} IAM role for this instance.".format(iam_policy)
                        except Exception as e:
                            final_string2[j] = "You haven't selected IAM role for this instance."
                        j+=1
                        try:
                            final_string2[j] = "You have attached a security group with id {} to this instance.".format(sg_id)
                        except Exception as e:
                            final_string2[j] = "You haven't attached a security group to this instance."
                        j+=1
                        if "22" in port:
                            final_string2[j] = "You have enabled SSH port for this instance."
                        else:
                            final_string2[j] = "You haven't enabled SSH port for this instance."
                        j+=1
                        try:
                            final_string2[j] = "You have created {} keypair for this instance.".format(keypair)
                        except Exception as e:
                            final_string2[j] = "You haven't created keypair for this instance."
                    except Exception as e:
                            print("Final result string creation failed because: ",e)

                    ec2_task_status["Instance:" +str(count_ec2)] = task_status2
                    ec2_finalresult["Instance:" +str(count_ec2)] = final_string2
                    count_ec2+=1

            except Exception as e:
                print("Listing ec2 instance failed because:",e)
            total_task_status["EC2 Instance"] = ec2_task_status
            complete_details["EC2 Instance"] = ec2_finalresult

        try:
            if "Success" in dax_status_flag and "Success" in ec2_status_flag:
                test_result["lab-validation-status"] = {"status" : "success"}
            else:
                test_result["lab-validation-status"] = {"status" : "failed"}
            test_result["lab-user-info"] = user_info
            test_result["lab-task-status"] = total_task_status
            test_result["lab-usertask-complete-details"] = complete_details
            
        except Exception as e:
            print("final try failed because ", e)
        
        print(test_result)  
        return(test_result)
        
    except Exception as e:
        print("Client connection failed because: ",e)
