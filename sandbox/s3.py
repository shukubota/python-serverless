import boto3
from botocore.config import Config
import pandas as pd
import io

AWS_PROFILE = 'localstack'
AWS_REGION = 'ap-northeast-1'
ENDPOINT = 'http://localhost:4566'

boto3.setup_default_session(profile_name=AWS_PROFILE)
s3 = boto3.client('s3', region_name=AWS_REGION, endpoint_url=ENDPOINT)

response = s3.get_object(Bucket="s3-test", Key="株式会社auditcheck_test.xlsx")
# print(response['Body'].read())
content = response['Body'].read()

# Filepath = os.path.abspath('mapping.xlsx') 
df = pd.read_excel(io.BytesIO(content), sheet_name='シート1')  
print(df)

# for bucket in s3.buckets.all():
#         print(bucket.name)
