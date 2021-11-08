import boto3

DryRun = True
ec2_client = boto3.client('ec2')
images = ec2_client.describe_images(
  Filters=[
        {
            'Name': 'name',
            'Values': [
                'amzn2-ami-hvm*',
            ]
        },
        {
            'Name': 'owner-alias',
            'Values': [
                'amazon',
            ]
        },
    ],
)
ec2_image = boto3.resource('ec2')
AMI = ec2_image.Image(images['Images'][0]['ImageId'])
if AMI.state == "available":
  print(AMI.image_id)
  instance = ec2_client.run_instances(
    ImageId=AMI.image_id,
    InstanceType='t2.micro',
    MaxCount=1,
    MinCount=1,
    DryRun=DryRun
  )
  ec2_instance = boto3.resource('ec2')
  ec2 = ec2_instance.Instance(instance['Instances'][0]['InstanceId'])
  print(ec2.instance_id)
  ec2.wait_until_running()
  print(f"Instance is {ec2.state['Name']}")
  ec2.terminate()
  ec2.wait_until_terminated()
  print(f"Instance is {ec2.state['Name']}")
else: 
  print("The AMI was not available")