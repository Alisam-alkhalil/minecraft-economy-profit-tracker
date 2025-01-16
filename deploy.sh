#!/bin/bash
set -x
# Variables
KEY_NAME="alisam-pipeline-key"  # Replace with an EC2 key pair name
S3_BUCKET_NAME="alisam-s3-deploy-bucket" # Replace with your desired S3 bucket name
LAMBDA_ZIP="lambda_function.zip"
PACKAGES="packages.zip"
WEBSITE_PY="./web/website.py"
STACK_NAME="my-cloudformation-stack"
REGION="eu-west-1"

set -e

echo "Checking if EC2 Key Pair $KEY_NAME exists..."
echo "Using AWS region: $(aws configure get region)"


# 1. Create EC2 Key Pair (will fail if it already exists)
echo "Creating EC2 Key Pair: $KEY_NAME"
aws ec2 create-key-pair --key-name "$KEY_NAME" --query "KeyMaterial" --output text > "$KEY_NAME.pem"
chmod 400 "$KEY_NAME.pem"

# 2. Create S3 Bucket (will fail if it already exists)
echo "Creating S3 Bucket: $S3_BUCKET_NAME"
aws s3 mb "s3://$S3_BUCKET_NAME" --region "$REGION"

echo "Disabling Block Public Access for S3 Bucket: $S3_BUCKET_NAME"
aws s3api put-public-access-block --bucket "$S3_BUCKET_NAME" --public-access-block-configuration \
    BlockPublicAcls=false,IgnorePublicAcls=false,BlockPublicPolicy=false,RestrictPublicBuckets=false

echo "Setting public access policy for S3 Bucket: $S3_BUCKET_NAME"
aws s3api put-bucket-policy --bucket "$S3_BUCKET_NAME" --policy '{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadGetObject",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::'"$S3_BUCKET_NAME"'/*"
    }
  ]
}'



# 3. Upload files to S3
echo "Uploading Lambda function, psycopg2 layer, and website.py to S3..."
aws s3 cp "$LAMBDA_ZIP" "s3://$S3_BUCKET_NAME/$LAMBDA_ZIP" --region "$REGION"
aws s3 cp "$PACKAGES" "s3://$S3_BUCKET_NAME/$PACKAGES"  --region "$REGION"
aws s3 cp "$WEBSITE_PY" "s3://$S3_BUCKET_NAME/website.py" --region "$REGION"

# 4. Deploy CloudFormation Stack
echo "Deploying CloudFormation Stack: $STACK_NAME"
if ! aws cloudformation deploy \
    --template-file cloudformation.yaml \
    --stack-name "$STACK_NAME" \
    --capabilities CAPABILITY_NAMED_IAM \
    --parameter-overrides \
        KeyName="$KEY_NAME" \
        S3BucketName="$S3_BUCKET_NAME"; then
    echo "CloudFormation deploy failed, rolling back..."
    aws cloudformation delete-stack --stack-name "$STACK_NAME" || { echo "Rollback failed, manual intervention required."; exit 1; }
    exit 1
fi