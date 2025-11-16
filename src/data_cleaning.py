"""Data cleaning (simplified). Run from project root."""
import pandas as pd
import numpy as np
import re
def clean(input_path, output_path):
    df = pd.read_csv(input_path, low_memory=False)
    df.columns = [re.sub(r"\s+|[^0-9a-zA-Z_]","_",c).lower() for c in df.columns]
    if 'ticket_price_cr' in df.columns:
        df['ticket_price_cr'] = df['ticket_price_cr'].astype(str).str.replace(',','').str.extract(r'([0-9.]+)').astype(float)
        df['ticket_price_inr'] = df['ticket_price_cr'] * 1e7
    df.to_csv(output_path, index=False)
if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('--input', required=True)
    p.add_argument('--output', required=True)
    args = p.parse_args()
    clean(args.input, args.output)
