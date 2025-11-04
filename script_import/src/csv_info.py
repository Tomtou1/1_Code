import pandas as pd

def get_nbrline_csv(csv_path):
    df_csv = pd.read_csv(csv_path)
    return len(df_csv)
