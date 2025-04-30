#IMPORT DATA S3

import boto3
import pandas as pd
from io import StringIO

# Configure your AWS credentials (make sure you have aws configure or environment variables set up)
s3_client = boto3.client('s3')

# File parameters in S3
bucket_name = 'etl-satisf-data-p4'
file_key = 'restaurant_customer_satisfaction_clean.csv'

# Get the CSV file from S3
response = s3_client.get_object(Bucket=bucket_name, Key=file_key)
csv_data = response['Body'].read().decode('utf-8')

# Read the CSV with pandas
df = pd.read_csv(StringIO(csv_data))

# Show the first records to verify
print(df.head())
