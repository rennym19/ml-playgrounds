from json import loads

import pandas as pd

def parse_from_file(file):
    if file is None:
        return None

    df = pd.read_csv(file)
    json_data = loads(df.to_json(orient='records'))
    return json_data
