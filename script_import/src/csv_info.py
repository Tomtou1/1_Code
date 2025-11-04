import pandas as pd

def get_nbrline_csv(csv_path):
    df_csv = pd.read_csv(csv_path)
    return len(df_csv)

def get_nbrcolumns_csv(csv_path):
    df_csv = pd.read_csv(csv_path)
    return df_csv.shape[1]

def get_doublons_csv(csv_path):
    df_csv = pd.read_csv(csv_path)
    return df_csv.duplicated().sum()

def get_missing_data_csv(csv_path):
    df_csv = pd.read_csv(csv_path)
    return sum(df_csv.isna().sum())