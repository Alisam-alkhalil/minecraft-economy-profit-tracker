import os
import boto3
import json
from botocore.exceptions import ClientError
from src import extract, transform, load, schema


print("Getting Secret")
def get_secret():

    """
    Retrieves a secret from SecretsManager as well as hostname from RDS Instance
    """
    
    secret_name = "MyRDSSecret"
    region_name = "eu-west-1"

    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:

        raise e

    secret = get_secret_value_response['SecretString']

    rds_client = boto3.client('rds')
    db_instance_identifier = 'mypostgresdb'
    response = rds_client.describe_db_instances(DBInstanceIdentifier=db_instance_identifier)
    db_instance = response['DBInstances'][0]
    db_host = db_instance['Endpoint']['Address']

    return secret, db_host

secret, host = get_secret()
secret = json.loads(secret)

api_key = "405aca69-EXAMPLE-be27-EXAMPLEf271" # Enter your API Key here (This is an Example API Key)

url = "https://api.hypixel.net/skyblock/bazaar"

host = host
port = 5432
user = secret["username"]
password = secret["password"]
dbname = "postgres"

def lambda_handler(event, context):

    """
    The entry point for the AWS Lambda function.

    This function retrieves the latest data from the Hypixel Skyblock Bazaar API, transforms it to include profit metrics, sorts it by true hourly profit, and loads the top 500 items into the database.

    :param event: The event object passed to the AWS Lambda function
    :param context: The context object passed to the AWS Lambda function
    :return: A dictionary containing the HTTP status code, status message, headers, and body
    """

    products_list = extract.get_data(url, api_key)

    products_list = transform.get_profit_data(products_list)

    sorted_products = sorted(products_list,key = lambda x: x["true_hourly_profit"], reverse=True)

    schema.create_schema(host, port, user, password, dbname)

    load.load_data(sorted_products[:500], host, port, user, password, dbname)

    return {
        'statusCode': 200,
        'statusMessage': '200 OK',
        'headers': {
            'Content-Type': 'text/html; charset=UTF-8'
        },
        'body': '<p>Hello World</p>'
    }
