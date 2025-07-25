import boto3
import os
import re

def lambda_handler(event, context):
    # Get email from event
    email = event.get('email')
    if not email:
        return {'status': 'error', 'message': 'No email provided'}

    # Extract first name from email
    match = re.match(r"([a-zA-Z0-9]+)[._-]", email)
    if match:
        prefix = match.group(1)
    else:
        prefix = email.split('@')[0]

    # Get AWS account ID
    sts = boto3.client('sts')
    account_id = sts.get_caller_identity()['Account']

    # Resource name suffix
    suffix = account_id

    # SNS check
    sns = boto3.client('sns')
    topics = sns.list_topics()['Topics']
    expected_sns = [f"{prefix}-sns-{suffix}" for i in range(1, 4)]
    found_sns = [t['TopicArn'].split(':')[-1] for t in topics if t['TopicArn'].split(':')[-1].startswith(f"{prefix}-sns-") and t['TopicArn'].split('-')[-1] == suffix]
    sns_ok = len(found_sns) == 3

    # SQS check
    sqs = boto3.client('sqs')
    queues = sqs.list_queues()['QueueUrls']
    expected_sqs = f"{prefix}-queue-{suffix}"
    found_sqs = [q for q in queues if q.split('/')[-1] == expected_sqs]
    sqs_ok = len(found_sqs) == 1

    # S3 bucket check
    s3 = boto3.client('s3')
    expected_bucket = f"{prefix}-bucket-{suffix}"
    buckets = s3.list_buckets()['Buckets']
    found_bucket = any(b['Name'] == expected_bucket for b in buckets)

    # S3 object check
    object_ok = False
    if found_bucket:
        try:
            obj = s3.get_object(Bucket=expected_bucket, Key='my_upload.txt')
            content = obj['Body'].read().decode('utf-8').strip()
            object_ok = content == "hi, from terraform"
        except Exception:
            object_ok = False

    result = {
        'sns_ok': sns_ok,
        'sqs_ok': sqs_ok,
        'bucket_ok': found_bucket,
        'object_ok': object_ok,
        'details': {
            'found_sns': found_sns,
            'found_sqs': found_sqs,
            'bucket': expected_bucket,
            'object_content': content if object_ok else None
        }
    }
    result['all_ok'] = all([sns_ok, sqs_ok, found_bucket, object_ok])
    return result
