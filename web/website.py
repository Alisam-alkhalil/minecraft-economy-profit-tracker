import matplotlib.pyplot as plt
import boto3
from botocore.exceptions import ClientError
import json
import streamlit as st
import psycopg2
import pandas as pd
import csv

def get_secret():

    """
    Retrieves a secret from SecretsManager
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

secret = json.loads(get_secret())

host = "database-2.ctaa6q06c3qp.eu-west-1.rds.amazonaws.com"
port = 5432
user = secret["username"]
password = secret["password"]
dbname = "postgres"

def create_webpage( host: str, port: int, user: str, password: str, dbname: str):

    """
    Connects to a PostgreSQL database and fetches data from the market_data table.

    Displays a title, a logo, and two plots of the most profitable products to flip, and their buy and sell prices over time.

    Parameters
    ----------
    host : str
        The hostname of the PostgreSQL database server.
    port : int
        The port number of the PostgreSQL database server.
    user : str
        The username to use when connecting to the PostgreSQL database server.
    password : str
        The password to use when connecting to the PostgreSQL database server.
    dbname : str
        The name of the PostgreSQL database to connect to.

    Returns
    -------
    None
    """

    with psycopg2.connect(host=host, port=port, user=user, password=password, dbname=dbname) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM market_data")
        data = cursor.fetchall()
        cursor.execute("SELECT * FROM market_data ORDER BY date DESC LIMIT 500")
        top_products = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(data, columns=columns)
        top_products = pd.DataFrame(top_products, columns=columns)

    st.set_page_config(layout="centered",page_title = "Minecraft Marketplace Profit Calculator")

    st.image("https://res.cloudinary.com/zenbusiness/image/upload/v1670445040/logaster/logaster-2020-06-image14-3.avif", use_column_width=True, width=300)

    st.title("Minecraft Marketplace Profit Calculator")

    st.title("Most Profitable Products to Flip 💵")
    
    top_products.rename(columns={"true_hourly_profit": "Adjusted Hourly Profit", "hourly_profit": "Max Hourly Profit", "product_id": "Product", "profit_per_item": "Profit Per Item"}, inplace=True)
    top_products = top_products[["Product","Adjusted Hourly Profit", "Max Hourly Profit", "sell_price", "buy_price", "Profit Per Item"]]

    st.dataframe(top_products, width=1500, height=400)

    st.title("Buy and Sell Prices 📈")

    product_options = df["product_id"].unique()

    selected_product = st.selectbox("Select a product", product_options)

    filtered_df = df[df["product_id"] == selected_product]

    plt.figure(figsize=(20, 12))
    plt.plot(filtered_df["date"], filtered_df["sell_price"], marker = "o", color = "red", label = "Sell Price")
    plt.xlabel("Product")
    plt.ylabel("Price")
    plt.title("Sell Price")
    plt.xticks(filtered_df["date"][::2], rotation=45) 
    plt.legend()
    st.pyplot(plt)

    plt.figure(figsize=(20, 12))
    plt.plot(filtered_df["date"], filtered_df["buy_price"], marker = "o", color = "blue", label = "Buy Price")
    plt.xlabel("Product")
    plt.ylabel("Price")
    plt.title("Buy Price")
    plt.xticks(filtered_df["date"][::2], rotation=45)  
    plt.legend()
    st.pyplot(plt)

if __name__ == "__main__":  
    create_webpage(host, port, user, password, dbname)