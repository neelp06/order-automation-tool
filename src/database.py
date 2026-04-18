import sqlite3
import pandas as pd

DB_PATH = '../data/orders.db'

def save_to_db(df):
    conn = sqlite3.connect(DB_PATH)
    df.to_sql('orders', conn, if_exists='replace', index=False)
    conn.close()
    print("✅ Orders saved to database.")

def get_all_orders():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql("SELECT * FROM orders", conn)
    conn.close()
    return df

def get_pending_orders():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql("SELECT * FROM orders WHERE status = 'Pending'", conn)
    conn.close()
    return df

def get_flagged_orders():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql("SELECT * FROM orders WHERE missing_data = 1 OR is_duplicate = 1", conn)
    conn.close()
    return df

# Run it
from ingest import load_orders

df = load_orders('../data/orders.csv')
save_to_db(df)

print("\n--- All Orders from Database ---")
print(get_all_orders())

print("\n--- Flagged Orders ---")
print(get_flagged_orders())