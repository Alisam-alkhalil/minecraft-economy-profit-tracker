# Minecraft Server Marketplace Tracker

This is a quick project which pulls marketplace data from a Minecraft server's API to analyse what are the most profitable items to buy and sell based on factors such as profit margins, competition, and buy and sell volumes.

It also records historic prices of each item to be able to forecast trends.

Currently, all data is hosted locally in a CSV file, but it will eventually be stored in a database and displayed on a simple Streamlit website. The data will be shown in tables and graphs, with pandas used to create a dataframe from the updated database content.