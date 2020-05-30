import pandas as pd

def parse_from_file(file):
    df = pd.read_csv(file)
    return df.to_json()
