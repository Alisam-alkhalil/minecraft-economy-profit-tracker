import requests

def get_data(url: str, api_key: str):
    """
    Retrieves data from the hypixel skyblock bazaar API.

    Args:
        url (str): The url of the hypixel skyblock bazaar API.
        api_key (str): The API key to use for the request.

    Returns:
        A list of dictionaries, where each dictionary is a product's quick status.
    """
    response = requests.get(url, headers={"API-Key": api_key})
    data = response.json()

    products = [x for x in data["products"]]

    return  [data["products"][x]["quick_status"] for x in products]
