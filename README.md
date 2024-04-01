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

## 2. Setup AWS Ressources

### 2.1. Network Access
- VPC

- get RouteTableId
```aws ec2 describe-route-tables | grep "RouteTableId"```
--> _rtb-08d8bcb788bb33983_ (stayed constant)

- get vpc id
```aws ec2 describe-vpcs | grep "VpcId"```
--> _vpc-022630960c2b48beb_ (stayed constant)

- S3 Gateway  
```BASH
aws ec2 create-vpc-endpoint --vpc-id _______ --service-name com.amazonaws.us-east-1.s3 --route-table-ids _______

aws ec2 create-vpc-endpoint --vpc-id vpc-022630960c2b48beb --service-name com.amazonaws.us-east-1.s3 --route-table-ids rtb-08d8bcb788bb33983
```

-->
```BASH
{
    "VpcEndpoint": {
        "VpcEndpointId": "vpce-02d9b861ebbd040a3",
        "VpcEndpointType": "Gateway",
        "VpcId": "vpc-022630960c2b48beb",
        "ServiceName": "com.amazonaws.us-east-1.s3",
        "State": "available",
        "PolicyDocument": "{\"Version\":\"2008-10-17\",\"Statement\":[{\"Effect\":\"Allow\",\"Principal\":\"*\",\"Action\":\"*\",\"Resource\":\"*\"}]}",
        "RouteTableIds": [
            "rtb-08d8bcb788bb33983"
        ],
        "SubnetIds": [],
        "Groups": [],
        "PrivateDnsEnabled": false,
        "RequesterManaged": false,
        "NetworkInterfaceIds": [],
        "DnsEntries": [],
        "CreationTimestamp": "2024-03-30T14:03:32+00:00",
        "OwnerId": "137423019814"
    }
}
```
--> endpoint id changes
- 2024/04/01: _vpce-0e38377f58f2d63ad_

--> we see it in AWS console in VPC / Endpoints
https://us-east-1.console.aws.amazon.com/vpcconsole/home?region=us-east-1#Endpoints:

### 2.2. User Privileges
- IAM Role with policies

- create glue service role
```BASH
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
--> we see it in IAM / Roles / my-glue-service-role

- attach policy 

    - s3 access
**Replace the blanks in the statement below with your S3 bucket name (ex: seans-lakehouse)**

    ```BASH
    aws iam put-role-policy --role-name my-glue-service-role --policy-name S3Access --policy-document '{ "Version": "2012-10-17", "Statement": [ { "Sid": "ListObjectsInBucket", "Effect": "Allow", "Action": [ "s3:ListBucket" ], "Resource": [ "arn:aws:s3:::_______" ] }, { "Sid": "AllObjectActions", "Effect": "Allow", "Action": "s3:*Object", "Resource": [ "arn:aws:s3:::_______/*" ] } ] }'


    aws iam put-role-policy --role-name my-glue-service-role --policy-name S3Access --policy-document '{ "Version": "2012-10-17", "Statement": [ { "Sid": "ListObjectsInBucket", "Effect": "Allow", "Action": [ "s3:ListBucket" ], "Resource": [ "arn:aws:s3:::p3-stedi-lakehouse/" ] }, { "Sid": "AllObjectActions", "Effect": "Allow", "Action": "s3:*Object", "Resource": [ "arn:aws:s3:::p3-stedi-lakehouse/*" ] } ] }'
    ```


    - glue access
    ```BASH
    aws iam put-role-policy --role-name my-glue-service-role --policy-name GlueAccess --policy-document '{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "glue:*",
                "s3:GetBucketLocation",
                "s3:ListBucket",
                "s3:ListAllMyBuckets",
                "s3:GetBucketAcl",
                "ec2:DescribeVpcEndpoints",
                "ec2:DescribeRouteTables",
                "ec2:CreateNetworkInterface",
                "ec2:DeleteNetworkInterface",
                "ec2:DescribeNetworkInterfaces",
                "ec2:DescribeSecurityGroups",
                "ec2:DescribeSubnets",
                "ec2:DescribeVpcAttribute",
                "iam:ListRolePolicies",
                "iam:GetRole",
                "iam:GetRolePolicy",
                "cloudwatch:PutMetricData"
            ],
            "Resource": [
                "*"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:CreateBucket",
                "s3:PutBucketPublicAccessBlock"
            ],
            "Resource": [
                "arn:aws:s3:::aws-glue-*"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:PutObject",
                "s3:DeleteObject"
            ],
            "Resource": [
                "arn:aws:s3:::aws-glue-*/*",
                "arn:aws:s3:::*/*aws-glue-*/*"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject"
            ],
            "Resource": [
                "arn:aws:s3:::crawler-public*",
                "arn:aws:s3:::aws-glue-*"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents",
                "logs:AssociateKmsKey"
            ],
            "Resource": [
                "arn:aws:logs:*:*:/aws-glue/*"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "ec2:CreateTags",
                "ec2:DeleteTags"
            ],
            "Condition": {
                "ForAllValues:StringEquals": {
                    "aws:TagKeys": [
                        "aws-glue-service-resource"
                    ]
                }
            },
            "Resource": [
                "arn:aws:ec2:*:*:network-interface/*",
                "arn:aws:ec2:*:*:security-group/*",
                "arn:aws:ec2:*:*:instance/*"
            ]
        }
    ]
}'
    ```

### 2.5. Create S3 buckets
```BASH
aws s3 mb s3://p3-stedi-lakehouse/customer/landing/
aws s3 mb s3://p3-stedi-lakehouse/customer/trusted/
aws s3 mb s3://p3-stedi-lakehouse/customer/curated/

aws s3 mb s3://p3-stedi-lakehouse/step_trainer/landing/
aws s3 mb s3://p3-stedi-lakehouse/step_trainer/trusted/
aws s3 mb s3://p3-stedi-lakehouse/step_trainer/curated/

aws s3 mb s3://p3-stedi-lakehouse/accelerometer/landing/
aws s3 mb s3://p3-stedi-lakehouse/accelerometer/trusted/
aws s3 mb s3://p3-stedi-lakehouse/accelerometer/curated/
```


### 2.4. After usage: delete the ressources

- delete the vpc endpoint
```aws ec2 delete-vpc-endpoints --vpc-endpoint-ids vpce-02d9b861ebbd040a3```

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

- delete the buckets
```BASH
aws s3 rb s3://p3-stedi-lakehouse/customer/landing/ --force
aws s3 rb s3://p3-stedi-lakehouse/customer/trusted/ --force
aws s3 rb s3://p3-stedi-lakehouse/curated/curated/ --force

aws s3 rb s3://p3-stedi-lakehouse/step_trainer/landing/ --force
aws s3 rb s3://p3-stedi-lakehouse/step_trainer/trusted/ --force
aws s3 rb s3://p3-stedi-lakehouse/step_trainer/curated/ --force

aws s3 rb s3://p3-stedi-lakehouse/accelerometer/landing/ --force
aws s3 rb s3://p3-stedi-lakehouse/accelerometer/trusted/ --force
aws s3 rb s3://p3-stedi-lakehouse/accelerometer/curated/ --force
```


## 3. Landing Zone
- Sources
s3://cd0030bucket/customers/
s3://cd0030bucket/step_trainer/
s3://cd0030bucket/accelerometer/


- ingest data
    see:
    https://learn.udacity.com/nanodegrees/nd027/parts/cd12441/lessons/5dcc7706-1ab5-4361-9b6b-59d8531a41b8/concepts/8443a918-363a-4048-83e9-476d33ac6c95

    https://learn.udacity.com/nanodegrees/nd027/parts/cd12441/lessons/b197ec56-711e-40f4-8ce5-57bab539b408/concepts/4e1be55b-65b9-442f-9530-d036514873f2


    - clone git repo
    ```git clone https://github.com/udacity/nd027-Data-Engineering-Data-Lakes-AWS-Exercises.git```

        
    ```cd nd027-Data-Engineering-Data-Lakes-AWS-Exercises/project/starter```

    - upload to landing zone
    ```BASH
    aws s3 cp ./project/starter/customer/landing/customer-1691348231425.json s3://_______/customer/landing/

    cd customer/landing
    aws s3 cp ./customer-1691348231425.json s3://p3-stedi-lakehouse/customer/landing/
    cd ..

    cd step_trainer    
    aws s3 cp ./landing s3://p3-stedi-lakehouse/step_trainer/landing/ --recursive
    cd ..

    cd accelerometer
    aws s3 cp ./landing s3://p3-stedi-lakehouse/accelerometer/landing/ --recursive
    cd ..
    ```

    - delete source git clone
    ```BASH
    rm -r nd027-Data-Engineering-Data-Lakes-AWS-Exercises
    ```



- create table
    - aws glue / data catalog / databases
        - data 
    - --> in console search "glue data catalog"
    - add **database**
        - create database "_stedi_"
    - click on database stedi and add table: customer_landing
        - add columns
        - --> edit schema as JSON --> see _customer_landing.json_

    - --> alternatively we can create a table with athena
        --> advantage: we can save the create query
        <red> **note that we can create the DDL after a table was created (with glue) in Athena**</red>

- target tables
    - customer_landing
        - source: s3://p3-stedi-lakehouse/customer/landing/
    - accelerometer_landing
        - source: s3://p3-stedi-lakehouse/accelerometer/landing/
    - step_trainer_landing
        - source: s3://p3-stedi-lakehouse/step_trainer/landing/


- to remove
    - remove all tables (Athena or glue)
    - remove database (glue)

- query table
    - --> **Athena**



## 4. Trusted Zone

https://learn.udacity.com/nanodegrees/nd027/parts/cd12441/lessons/b197ec56-711e-40f4-8ce5-57bab539b408/concepts/37b447a5-9973-4613-bdff-a7311b07ec55

- glue jobs
    --> we can have multiple jobs, we can duplicate
    - pattern bucket : transform : bucket
    - at a drop fields or drup duplicates transform if needed

queries prepared in /trusted

_Note_ for step_trainer_trusted we first need customer_curated (step 3) --> see project rubric

## 5. Curated Zone
- tables
- customer
- machine learing