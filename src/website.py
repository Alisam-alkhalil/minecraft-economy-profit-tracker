import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import csv

def create_webpage(data: csv, sorted_products: list):

    """
    Creates a Streamlit webpage with the given data and sorted products.

    Args:
        data (csv): The path to the csv file containing the product data.
        sorted_products (list): A list of dictionaries, each containing the product data sorted by true_hourly_profit.

    Returns:
        None
    """
    st.image("https://logos-world.net/wp-content/uploads/2023/12/Hypixel-Symbol.png")
    st.title("Skyblock Bazaar Profit Calculator")

    st.title("Most Profitable Products to Flip 💵")

    top_products = pd.DataFrame(sorted_products)
    top_products.rename(columns={"true_hourly_profit": "Adjusted Hourly Profit", "hourly_profit": "Max Hourly Profit", "productId": "Product", "profit_per_item": "Profit Per Item"}, inplace=True)
    top_products = top_products[["Product","Adjusted Hourly Profit", "Max Hourly Profit", "sellPrice", "buyPrice", "Profit Per Item"]]

    st.dataframe(top_products, width=900, height=400)

    st.title("Buy and Sell Prices 📈")

    df = pd.read_csv(data)

    product_options = df["productId"].unique()

    selected_product = st.selectbox("Select a product", product_options)


    filtered_df = df[df["productId"] == selected_product]


    plt.figure(figsize=(10, 6))
    plt.plot(filtered_df["date"], filtered_df["sellPrice"], marker = "o", color = "red", label = "Sell Price")
    plt.xlabel("Product")
    plt.ylabel("Price")
    plt.title("Sell Price")
    plt.xticks(filtered_df["date"][::2], rotation=45) 
    plt.legend()
    st.pyplot(plt)

    plt.figure(figsize=(10, 6))
    plt.plot(filtered_df["date"], filtered_df["buyPrice"], marker = "o", color = "blue", label = "Buy Price")
    plt.xlabel("Product")
    plt.ylabel("Price")
    plt.title("Buy Price")
    plt.xticks(filtered_df["date"][::2], rotation=45)  
    plt.legend()
    st.pyplot(plt)