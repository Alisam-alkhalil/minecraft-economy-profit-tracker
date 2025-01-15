import psycopg2

def create_schema(host: str, port: int, user: str, password: str, dbname: str):
    """
    Establish a connection to a PostgreSQL database and create a table named
    'market_data' if it does not already exist. The table contains columns for
    storing various attributes of market data including product ID, sell price,
    sell volume, buy price, buy volume, and other metrics related to sales and
    profitability.

    Parameters:
    host (str): The database server host.
    port (int): The port number for the database connection.
    user (str): The username for authenticating with the database.
    password (str): The password for authenticating with the database.
    dbname (str): The name of the database to connect to.
    """

    with psycopg2.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        dbname=dbname
    ) as conn:
        
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS market_data (
            id SERIAL PRIMARY KEY,
            product_id VARCHAR(255) NOT NULL,
            sell_price NUMERIC NOT NULL,
            sell_volume NUMERIC NOT NULL,
            sell_moving_week NUMERIC NOT NULL,
            sell_orders NUMERIC NOT NULL,
            buy_price NUMERIC NOT NULL,
            buy_volume NUMERIC NOT NULL,
            buy_moving_week NUMERIC NOT NULL,
            buy_orders NUMERIC NOT NULL,
            hourly_profit NUMERIC NOT NULL,
            competition NUMERIC NOT NULL,
            true_hourly_profit NUMERIC NOT NULL,
            profit_per_item NUMERIC NOT NULL,
            date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        """)
