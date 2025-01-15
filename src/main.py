import os
import requests
import json
import pandas as pd
import time
import matplotlib.pyplot as plt
import streamlit as st
import csv
from dotenv import load_dotenv
from datetime import datetime
import extract, transform, load, website

load_dotenv()

api_key = os.getenv("API_KEY")
url = os.getenv("URL")


products_list = extract.get_data(url, api_key)
products_list = transform.get_profit_data(products_list)
sorted_products = sorted(products_list,key = lambda x: x["true_hourly_profit"], reverse=True)

load.load_data(sorted_products[:500])




# print(json.dumps(sorted_products[0:10], indent=4))




website.create_webpage("../data.csv", sorted_products[:500])


