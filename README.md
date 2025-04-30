# Project-4-Basic-Data-Pipeline-
(On-Premise or Cloud) Simulate real data flow.

1. Introduction
This project simulates a real-world data pipeline that extracts, transforms, and loads customer satisfaction data from a restaurant business. The primary objective is to clean and encode the data, monitor the ETL process, and store the final dataset in an AWS S3 bucket. The processed data is later used for reporting and visualization in Power BI, providing actionable insights.

2. Dataset Description
The dataset used is restaurant_customer_satisfaction.csv, containing customer feedback information, including:
•	CustomerID
•	Gender
•	VisitFrequency
•	PreferredCuisine
•	TimeOfVisit
•	DiningOccasion
•	MealType
•	Satisfaction metrics
The dataset originated from a local file and was processed and uploaded to an AWS S3 bucket for further analysis.

3. Tools Used
•	Python: Main scripting language for ETL processes
•	Pandas: Data manipulation and cleaning
•	Scikit-learn: Label encoding of categorical data
•	Boto3: AWS SDK for Python, used to interact with S3 and CloudWatch
•	AWS S3: Cloud storage for the processed dataset
•	AWS CloudWatch: Logging and error tracking
•	Power BI: Data visualization and reporting platform

4. Development (Code)
The solution consists of three main Python scripts and a Power BI dashboard:
•	ETL_Satisf_Restaurant.py:
o	Loaded the raw CSV file
o	Cleaned and encoded multiple categorical features
o	Removed duplicates and null values
o	Logged each step to AWS CloudWatch
o	Uploaded the cleaned dataset to the S3 bucket etl-satisf-data-p4
•	ImportDataS3.py:
o	Connected to S3
o	Downloaded and verified the uploaded cleaned CSV
o	Loaded the file into a Pandas DataFrame
•	PruebasCloudWatch.py:
o	Created and tested CloudWatch log groups and log streams
o	Sent test logs to validate the monitoring setup
•	CustomerSatisfactionBoard.pbix:
o	Power BI dashboard built from the cleaned dataset stored in S3
o	Visualizations include satisfaction ratings by gender, meal type, and visit frequency

5. Results or Conclusions
•	Full ETL pipeline created, integrating on-premise and cloud resources
•	Successful implementation of logging using AWS CloudWatch for better observability
•	Cleaned and structured dataset uploaded to AWS S3 for centralized access
•	Power BI dashboard provides real-time insights into customer satisfaction

Key Learnings:
•	Designing and implementing cloud-based ETL workflows
•	Importance of logging and monitoring with CloudWatch
•	Integration between AWS, Python, and Power BI for end-to-end data pipeline solutions

6. GitHub Repository Structure
project4-data-pipeline/
├── ETL_Satisf_Restaurant.py           # Main ETL script
├── ImportDataS3.py                   # Script to download and verify data from S3
├── PruebasCloudWatch.py              # Script to test CloudWatch logging
├── CustomerSatisfactionBoard.pbix    # Power BI dashboard (only table)
├── README.md                         # Project documentation

Author
Monica Prieto — Data Engineer
