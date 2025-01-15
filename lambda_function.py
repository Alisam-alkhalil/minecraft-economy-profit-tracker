import os
import boto3
import json
from botocore.exceptions import ClientError
from src import extract, transform, load, schema
import logging

print("Getting Secret")
def get_secret():

    """
    Retrieves a secret from SecretsManager
    :return: The secret, as a string
    """
    secret_name = "rds!db-f2ac396a-647d-40e6-8679-e3f09a55af7e"
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

    return secret

print("Secret Obtained")
secret = json.loads(get_secret())

logger = logging.getLogger()
logging.basicConfig(level=logging.DEBUG)

logger.info("Retrieving API Key")
api_key = "405aca69-4266-474f-be27-0c6b55fdf271"
logger.info("Retrieving URL")
url = "https://api.hypixel.net/skyblock/bazaar"

host = "database-2.ctaa6q06c3qp.eu-west-1.rds.amazonaws.com"
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
    print("Starting Lambda")
    print("Extracting Live Data")
    products_list = extract.get_data(url, api_key)

    print("Transforming Data")
    products_list = transform.get_profit_data(products_list)

    print("Sorting Data")
    sorted_products = sorted(products_list,key = lambda x: x["true_hourly_profit"], reverse=True)

    print("Creating Database")
    schema.create_schema(host, port, user, password, dbname)

    print("Loading Data")
    load.load_data(sorted_products[:500], host, port, user, password, dbname)

    return {
        'statusCode': 200,
        'statusMessage': '200 OK',
        'headers': {
            'Content-Type': 'text/html; charset=UTF-8'
        },
        'body': '<p>Hello World</p>'
    }
