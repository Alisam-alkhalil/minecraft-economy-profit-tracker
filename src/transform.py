from datetime import datetime

def get_profit_data(products_list: list):
    """
    Calculates and adds profit-related metrics to each product in the list.

    For each product, computes the following:
    - hourly_profit: Estimated hourly profit based on buying and selling prices.
    - competition: Ratio of buy and sell volumes indicating market competition.
    - true_hourly_profit: Adjusted hourly profit considering competition level.
    - profit_per_item: Difference between buy and sell prices.
    - date: Timestamp of the calculation.

    Args:
        products_list (list): A list of product dictionaries with buy/sell data.

    Returns:
        list: The input list with added profit-related metrics for each product.
    """

    for x in range(len(products_list)):

        hourly_profit = round((min(products_list[x]["buyMovingWeek"], products_list[x]["sellMovingWeek"]) * (products_list[x]["buyPrice"] - products_list[x]["sellPrice"])) / 168, 2)

        try:
            competition = min(products_list[x]["buyVolume"], products_list[x]["sellVolume"]) / max(products_list[x]["buyVolume"], products_list[x]["sellVolume"])
        except ZeroDivisionError:
            compeition = 0

        true_hourly_profit = round(hourly_profit * competition, 2)

        profit_per_item = round(products_list[x]["buyPrice"] - products_list[x]["sellPrice"],2)

        products_list[x]["hourly_profit"] = hourly_profit
        products_list[x]["competition"] = competition
        products_list[x]["true_hourly_profit"] = true_hourly_profit
        products_list[x]["profit_per_item"] = profit_per_item
        products_list[x]["date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return products_list