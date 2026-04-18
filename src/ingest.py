import pandas as pd

def load_orders(filepath):
    # Read the CSV file
    df = pd.read_csv(filepath)
    
    # Flag rows with missing data
    df['missing_data'] = df.isnull().any(axis=1)
    
    # Flag duplicate order IDs
    df['is_duplicate'] = df.duplicated(subset='order_id', keep=False)
    
    return df

# Run it
df = load_orders('../data/orders.csv')
print(df)
print("\n--- Problem Orders ---")
print(df[df['missing_data'] | df['is_duplicate']])