import pandas as pd


def read_xlsx(filepath):
    df = pd.read_excel(filepath)
    df.dropna(inplace=True)

    return df.values.tolist()
