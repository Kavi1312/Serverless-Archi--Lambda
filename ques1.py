import boto3
import logging

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')
    
    # Get all EC2 instances
    response = ec2.describe_instances(Filters=[
        {'Name': 'tag:Action', 'Values': ['Auto-Stop', 'Auto-Start']}
    ])
    
    # Initialize lists for instances to start and stop
    auto_stop_instances = []
    auto_start_instances = []
    
    # Process the response
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            for tag in instance.get('Tags', []):
                if tag['Key'] == 'Action' and tag['Value'] == 'Auto-Stop':
                    auto_stop_instances.append(instance['InstanceId'])
                elif tag['Key'] == 'Action' and tag['Value'] == 'Auto-Start':
                    auto_start_instances.append(instance['InstanceId'])
    
    # Stop instances with 'Auto-Stop' tag
    if auto_stop_instances:
        logger.info(f"Stopping instances: {auto_stop_instances}")
        ec2.stop_instances(InstanceIds=auto_stop_instances)
    else:
        logger.info("No instances found with 'Auto-Stop' tag.")
    
    # Start instances with 'Auto-Start' tag
    if auto_start_instances:
        logger.info(f"Starting instances: {auto_start_instances}")
        ec2.start_instances(InstanceIds=auto_start_instances)
    else:
        logger.info("No instances found with 'Auto-Start' tag.")
    
    return {
        "statusCode": 200,
        "body": "Instance management completed successfully!"
    }
