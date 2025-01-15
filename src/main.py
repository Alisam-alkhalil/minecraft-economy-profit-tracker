import os
from dotenv import load_dotenv
import extract, transform, load

load_dotenv()

api_key = os.getenv("API_KEY")
url = os.getenv("URL")


if __name__ == "__main__":

    products_list = extract.get_data(url, api_key)
    products_list = transform.get_profit_data(products_list)
    sorted_products = sorted(products_list,key = lambda x: x["true_hourly_profit"], reverse=True)
    load.load_data(sorted_products[:500])




