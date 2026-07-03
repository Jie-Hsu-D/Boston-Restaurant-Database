import os
from dotenv import load_dotenv
import mysql.connector
import pandas as pd

load_dotenv()

conn = mysql.connector.connect(
    host=os.getenv("MYSQL_HOST"),
    port=int(os.getenv("MYSQL_PORT")),
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    database=os.getenv("MYSQL_DATABASE")
)

tables = pd.read_sql("SHOW TABLES", conn)
print("Tables:")
print(tables)

for table_name in tables.iloc[:, 0]:
    print(f"\n--- {table_name} type ---")
    columns = pd.read_sql(f"DESCRIBE {table_name}", conn)
    print(columns[['Field', 'Type']])

conn.close()