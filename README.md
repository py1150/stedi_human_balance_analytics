# stedi_human_balance_analytics
Udacity Nanodegree Data Engineering with AWS Project 3

## Setup / Target

- Landing
    - glue jobs
- Trusted
    - glue jobs
- Curated


- for glue jobs (names see rubric)
    - see https://learn.udacity.com/nanodegrees/nd027/parts/cd12441/lessons/5dcc7706-1ab5-4361-9b6b-59d8531a41b8/concepts/1973f145-8bae-40d7-93e3-f245730c96a5
        - Glue / ETL jobs / Visual ETL

    - https://learn.udacity.com/nanodegrees/nd027/parts/cd12441/lessons/5dcc7706-1ab5-4361-9b6b-59d8531a41b8/concepts/8443a918-363a-4048-83e9-476d33ac6c95

    - output of gluejobs can be stored as code ....py
- Note: best to use queries for the job nodes

- directory structured: s3://name/table/landing...



_ingest data and select only approved_


![below](/Cyber/Courses/Udacity_DataEng/_pic/stedi_workflow.png "Project workflow")

- Landing
    - S3 buckets
        output:
        - customer_landing
        - accelerometer_landing
        - step_trainer_landing

    - define tables
        - glue console
            --> data catalog
            - add table - add path
            - add format
            - add columns and data types
                (in exercise we used BigInt for share with flag and dates)
            - --> now table is in glue catalog --> search with AThena is possible
            - --> **we can query the data before loading them**
    - ingest data (landing zone)
        - to obtain data - in aws shell clone git rep - go to /starter
        
        - create s3 buckets
        - copy data: ```aws s3 cp source s3://target-bucket/```
        - list them ```aws s3 ls s3://...```
        - --> create a glue table from the ingested data
            --> query
        - --> alternatively we can also create the table (manually) directly in Athena to query
         --> we get **create table queries** in the preview which we can save
- process data (trusted zone)
        - two steps
            - join and 
            - filter
        - see videos
- finalize data (curated zone)
    - join multiple data sources / apply transformations (short note in video 12)

    - join cusotmer_trusted and 
        - accelerometer_trusteted by _email_
        - output should only have columns from the customer table

- Security
    - we need an Endpoint that will allow Glue to reach out to S3
    - 1. **Network Access**: VPC
    - 2. **User Privileges** (for Glue to perform tasks on data within network): IAM ROle ```aws iam create-role --role-name my-glue-service-role --assume -role-policy-document .....```
        - add privileges to role ```aws iam --role-name my-glue service-role --policy-name S3 Access --policy-document...```
            --> wrong syntax
        - ```aws iam put-role-policy --role-name my-glue-service-role --policy-name S3Access --policy-document```
        - ```aws iam put-role-policy --role-name my-glue-service-role --policy-name GlueAccess --policy-document```

## Data

### 1. Customer Records

s3://cd0030bucket/customers/

serialnumber
sharewithpublicasofdate
birthday
registrationdate
sharewithresearchasofdate
customername
email
lastupdatedate
phone
sharewithfriendsasofdate

### 2. Step Trainer Records

This is the data from the motion sensor.

s3://cd0030bucket/step_trainer/

sensorReadingTime
serialNumber
distanceFromObject


### 3. Accelerometer Records

This is the data from the mobile app.

timeStamp
user
x
y
z



## 1. Workflow

- 1. Security Setup
- 2. Landing Zone
- 3. Trusted Zone
- 4. Curated Zone

## 2. Security Setup

### 2.1. Network Access
- VPC

- get RouteTableId
```aws ec2 describe-route-tables```

- get vpc id
```aws ec3 describe-vpcs```

- S3 Gateway  
```BASH
aws ec2 create-vpc-endpoint --vpc-id _______ --service-name com.amazonaws.us-east-1.s3 --route-table-ids _______
```

### 2.2. User Privileges
- IAM Role with policies

- create glue service role
```PYTHON
aws iam create-role --role-name my-glue-service-role --assume-role-policy-document '{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Service": "glue.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }
    ]
}'
```

- attach policy 

    - s3 access
**Replace the blanks in the statement below with your S3 bucket name (ex: seans-lakehouse)**

    ```BASH
    aws iam put-role-policy --role-name my-glue-service-role --policy-name S3Access --policy-document '{ "Version": "2012-10-17", "Statement": [ { "Sid": "ListObjectsInBucket", "Effect": "Allow", "Action": [ "s3:ListBucket" ], "Resource": [ "arn:aws:s3:::_______" ] }, { "Sid": "AllObjectActions", "Effect": "Allow", "Action": "s3:*Object", "Resource": [ "arn:aws:s3:::_______/*" ] } ] }'
    ```


    - glue access
    ```BASH
    aws iam put-role-policy --role-name my-glue-service-role --policy-name GlueAccess --policy-document
    ```

### 2.3. After usage: delete the ressources

- delete the vpc endpoint
```aws ec2 delete-vpc-endpoints --vpc-endpoint-ids vpce-aa22bb33 vpce-1a2b3c4d```

(check in AWS console)


- delete an IAM role

```BASH
detach-role-policy --role-name <value> --policy-arn <value>
delete-role --role-name <value>
```

```PYTHON
iam.detach_role_policy(RoleName=DWH_IAM_ROLE_NAME, PolicyArn="arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess")
iam.delete_role(RoleName=DWH_IAM_ROLE_NAME)
```

- Note: for access with Python:
```PYTHON
import boto3

ec2 = boto3.resource('ec2',
                       region_name="us-west-2",
                       aws_access_key_id=KEY,
                       aws_secret_access_key=SECRET
                    )

s3 = boto3.resource('s3',
                       region_name="us-west-2",
                       aws_access_key_id=KEY,
                       aws_secret_access_key=SECRET
                   )

iam = boto3.client('iam',aws_access_key_id=KEY,
                     aws_secret_access_key=SECRET,
                     region_name='us-west-2'
                  )
```



## 3. Landing Zone
## 4. Trusted Zone
## 5. Curated Zone