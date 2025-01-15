import psycopg2

def load_data(products_list: list, host: str, port: int, user: str, password: str, dbname: str):

    """
    Loads the given list of products into the market_data table in the
    specified PostgreSQL database.

    :param products_list: A list of product dictionaries with the same
        structure as the return value of get_profit_data.
    :param host: The hostname of the PostgreSQL server.
    :param port: The port the PostgreSQL server is listening on.
    :param user: The username to use when connecting to the PostgreSQL
        server.
    :param password: The password to use when connecting to the PostgreSQL
        server.
    :param dbname: The name of the database to use.
    """
    values = [ (
        product['productId'],
        product['sellPrice'],
        product['sellVolume'],
        product['sellMovingWeek'],
        product['sellOrders'],
        product['buyPrice'],
        product['buyVolume'],
        product['buyMovingWeek'],
        product['buyOrders'],
        product['hourly_profit'],
        product['competition'],
        product['true_hourly_profit'],
        product['profit_per_item'],
        product['date']
        ) for product in products_list ]

    with psycopg2.connect(host=host, port=port, user=user, password=password, dbname=dbname) as conn:
        cursor = conn.cursor()
        cursor.executemany("""
            INSERT INTO market_data (
                product_id,
                sell_price,
                sell_volume,
                sell_moving_week,
                sell_orders,
                buy_price,
                buy_volume,
                buy_moving_week,
                buy_orders,
                hourly_profit,
                competition,
                true_hourly_profit,
                profit_per_item,
                date) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, values
            )