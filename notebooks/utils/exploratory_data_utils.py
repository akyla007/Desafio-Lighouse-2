import pandas as pd
import os
import sys
module_path = os.path.abspath(os.path.join(os.pardir))
if module_path not in sys.path:
    sys.path.append(module_path)

def remove_columns(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    return df.drop(columns=columns)


def get_bairro_mean_price(df: pd.DataFrame, bairro: list) -> pd.DataFrame:
    for b in bairro:
        mean_price = df[df["bairro"] == b]["price"].mean()
        df.loc[df["bairro"] == b, 'media_bairro'] = mean_price
    return df

def convert_boolean_columns_to_int(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    for column in columns:
        if column in df.columns:
            df[column] = df[column].astype(int)
    return df