import psycopg

with psycopg.connect(
    host="database-2.ctaa6q06c3qp.eu-west-1.rds.amazonaws.com",
    dbname="postgres",
    user="postgres",
    password="xnya4*y#JbQ)Abkx:SxCvB-(>bq4",
    port = 5432
    ) as conn:
    cursor = conn.cursor()

    cursor.execute("""
            CREATE TABLE IF NOT EXISTS market_data (
                id SERIAL PRIMARY KEY,
                product_id VARCHAR(255) NOT NULL,
                sell_price DECIMAL(10,2) NOT NULL,
                sell_volume DECIMAL(10,2) NOT NULL,
                sell_moving_week DECIMAL(10,2) NOT NULL,
                sell_orders DECIMAL(10,2) NOT NULL,
                buy_price DECIMAL(10,2) NOT NULL,
                buy_volume DECIMAL(10,2) NOT NULL,
                buy_moving_week DECIMAL(10,2) NOT NULL,
                buy_orders DECIMAL(10,2) NOT NULL,
                hourly_profit DECIMAL(10,2) NOT NULL,
                competition DECIMAL(10,2) NOT NULL,
                true_hourly_profit DECIMAL(10,2) NOT NULL,
                profit_per_item DECIMAL(10,2) NOT NULL,
                date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
            );
        """)
