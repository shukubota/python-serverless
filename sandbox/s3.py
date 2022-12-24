import boto3
from botocore.config import Config

AWS_PROFILE = 'localstack'
AWS_REGION = 'ap-northeast-1'
ENDPOINT = 'http://localhost:4566'

boto3.setup_default_session(profile_name=AWS_PROFILE)
s3 = boto3.resource('s3', region_name=AWS_REGION, endpoint_url=ENDPOINT)

for bucket in s3.buckets.all():
        print(bucket.name)
