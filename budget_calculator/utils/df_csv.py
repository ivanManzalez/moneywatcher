import pandas as pd

################################################################
def save_df_to_csv(dataframe, filepath):
  dataframe.to_csv(filepath, index=False)

def load_csv_to_df(filepath):
  return pd.read_csv(filepath)