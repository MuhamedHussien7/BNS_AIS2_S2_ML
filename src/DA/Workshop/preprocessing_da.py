import pandas as pd

def drop_columns(df, columns):
    return df.drop(columns=columns, errors='ignore')

def get_data_summary(df: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame({"Dtype": df.dtypes, "n_unique": df.nunique()}).T