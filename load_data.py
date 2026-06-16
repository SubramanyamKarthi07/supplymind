import pandas as pd
from sqlalchemy import create_engine

# PostgreSQL connection
engine = create_engine(
    'postgresql://postgres:skillvance2025@localhost:5432/postgres'
)

# CSV files and table names
tables = {
    'suppliers': 'suppliers.csv',
    'skus': 'skus.csv',
    'purchase_orders': 'purchase_orders.csv',
    'demand_history': 'demand_history.csv',
    'inventory_positions': 'inventory_positions.csv',
    'supplier_performance': 'supplier_performance.csv'
}

# Load each CSV into PostgreSQL
for table, file in tables.items():
    df = pd.read_csv(f'data/raw/{file}')

    # Create table and insert data
    df.to_sql(table, engine, if_exists='replace', index=False)

    print(f"{table} loaded — {len(df)} rows")