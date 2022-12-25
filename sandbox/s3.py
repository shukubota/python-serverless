import boto3
from botocore.config import Config
import pandas as pd
import io
import openpyxl as px

AWS_PROFILE = 'localstack'
AWS_REGION = 'ap-northeast-1'
ENDPOINT = 'http://localhost:4566'

boto3.setup_default_session(profile_name=AWS_PROFILE)
s3 = boto3.client('s3', region_name=AWS_REGION, endpoint_url=ENDPOINT)

response = s3.get_object(Bucket="s3-test", Key="株式会社auditcheck_test.xlsx")
# print(response['Body'].read())
content = response['Body'].read()

# Filepath = os.path.abspath('mapping.xlsx') 
df = pd.read_excel(io.BytesIO(content))  
print(df)
print(df.size)

bucket = 'your-s3-bucketname'
filepath = 'test_output.xlsx'
# df = pd.DataFrame({'Data': [10, 20, 30, 20, 15, 30, 45]})

with io.BytesIO() as output:
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, 'sheet_name')
    data = output.getvalue()
s3.put_object(Bucket="s3-test", Key=filepath, Body=data)


# filepath = f'test_output.xlsx' 
# wb = px.load_workbook(filepath)

# wb.save()

# df.to_excel(filepath)
# df.to_excel('s3://s3-test/output.xlsx')



# for bucket in s3.buckets.all():
#         print(bucket.name)
