import pandas as pd


def remove_columns(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    return df.drop(columns=columns)


def get_bairro_mean_price(df: pd.DataFrame, bairro: list) -> pd.DataFrame:
    for b in bairro:
        mean_price = df[df["bairro"] == b]["price"].mean()
        df.loc[df["bairro"] == b, 'media_bairro'] = mean_price
    return df