"""Load CSV to DB using SQLAlchemy."""
import pandas as pd
from sqlalchemy import create_engine
import sys
def load(csv_path, db_url, table='luxury_housing'):
    df = pd.read_csv(csv_path)
    engine = create_engine(db_url)
    df.to_sql(table, engine, if_exists='replace', index=False, method='multi', chunksize=1000)
if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('--input', required=True)
    p.add_argument('--db_url', required=True)
    args = p.parse_args()
    load(args.input, args.db_url)
