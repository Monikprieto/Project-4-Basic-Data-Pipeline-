# ETL Customer Satisfaction Restaurant

# Import libraries
import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
import boto3
import logging
import time

# Setup logging to AWS CloudWatch
logger = logging.getLogger()
logger.setLevel(logging.INFO)
cloudwatch = boto3.client('logs')
log_group = 'my-log-group'  
log_stream = 'my-log-stream' 

# Function to create the group and stream if it does not exist
def create_log_group_and_stream():
    try:
        # Check if the log group exists
        cloudwatch.describe_log_groups(logGroupNamePrefix=log_group)
    except cloudwatch.exceptions.ResourceNotFoundException:
        cloudwatch.create_log_group(logGroupName=log_group)
        print(f"Grupo de logs '{log_group}' creado.")
    
    try:
        # Check if the log stream exists
        cloudwatch.describe_log_streams(logGroupName=log_group, logStreamNamePrefix=log_stream)
    except cloudwatch.exceptions.ResourceNotFoundException:
        cloudwatch.create_log_stream(logGroupName=log_group, logStreamName=log_stream)
        print(f"Stream de logs '{log_stream}' creado.")

# Function to send logs to CloudWatch
def send_log_to_cloudwatch(message):
    cloudwatch.put_log_events(
        logGroupName=log_group,
        logStreamName=log_stream,
        logEvents=[
            {
                'timestamp': int(time.time() * 1000),  # Timestamp in milliseconds
                'message': message
            }
        ]
    )

# Call the function to create the group and stream
create_log_group_and_stream()

# Try-Except to handle ETL and alerts
try:
    # Load File CSV
    df = pd.read_csv('restaurant_customer_satisfaction.csv')
    send_log_to_cloudwatch('Data loaded successfully from CSV')
    print(df.head())

    # **CustomerID**: Check that it is unique (no need to transform, just check for duplicates)
    df['CustomerID'] = df['CustomerID'].astype(int)
    df = df.drop_duplicates(subset=['CustomerID'])
    send_log_to_cloudwatch('CustomerID column cleaned')

    # **Gender**: Code as a categorical variable
    df['Gender'] = df['Gender'].str.strip().str.capitalize()  # Normalize text (if there are spaces, capital letters)
    label_encoder = LabelEncoder()
    df['Gender'] = label_encoder.fit_transform(df['Gender'])  # Numeric coding
    send_log_to_cloudwatch('Gender column transformed')

    # **VisitFrequency**: Convert to ordinal values
    visit_mapping = {'Weekly': 3, 'Monthly': 2, 'Rarely': 1}
    df['VisitFrequency'] = df['VisitFrequency'].map(visit_mapping)
    send_log_to_cloudwatch('VisitFrequency column transformed')

    # **PreferredCuisine**: Normalize text
    df['PreferredCuisine'] = df['PreferredCuisine'].str.strip().str.capitalize()
    send_log_to_cloudwatch('PreferredCuisine column transformed')

    # **TimeOfVisit**: Convert to ordinal variables
    time_of_visit_mapping = {'Breakfast': 1, 'Lunch': 2, 'Dinner': 3}
    df['TimeOfVisit'] = df['TimeOfVisit'].map(time_of_visit_mapping)
    send_log_to_cloudwatch('TimeOfVisit column transformed')

    # **DiningOccasion**: Code as a categorical variable
    df['DiningOccasion'] = df['DiningOccasion'].str.strip().str.capitalize()
    df['DiningOccasion'] = label_encoder.fit_transform(df['DiningOccasion'])
    send_log_to_cloudwatch('DiningOccasion column transformed')

    # **MealType**: Code as a categorical variable
    df['MealType'] = df['MealType'].str.strip().str.capitalize()
    df['MealType'] = label_encoder.fit_transform(df['MealType'])
    send_log_to_cloudwatch('MealType column transformed')

    print(df.head())

    # Check for null values ​​in columns
    print(df.isnull().sum())
    send_log_to_cloudwatch('Checking for null values')
    
    # Remove rows with null values
    df = df.dropna()
    send_log_to_cloudwatch('Null values removed')

    print(df.isnull().sum())
    
    # Save cleaned data to CSV
    df.to_csv('restaurant_customer_satisfaction_clean.csv', index=False)
    send_log_to_cloudwatch('Cleaned data saved to CSV')

    # UPLOAD DATA TO AWS (S3)
    
    # Connect to AWS S3 Service
    s3 = boto3.client('s3')

    # Specifies the bucket name and file name
    bucket_name = 'etl-satisf-data-p4'
    file_name = 'restaurant_customer_satisfaction.csv'

    # Upload the CSV file to S3
    s3.upload_file('restaurant_customer_satisfaction_clean.csv', bucket_name, 'restaurant_customer_satisfaction_clean.csv')
    send_log_to_cloudwatch(f"File successfully uploaded to {bucket_name}/{file_name}")

except Exception as e:
    # Log error in CloudWatch if the process fails
    send_log_to_cloudwatch(f'Error in the ETL process: {str(e)}')
    logger.error(f'Error in the ETL process: {str(e)}')
