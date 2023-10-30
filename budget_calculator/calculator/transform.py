from statement_reader.vsa_statement_reader import statement_transactions_in
import pandas as pd

def estatements_to_df(directory, months, year):
  data = pd.DataFrame()
  
  for month in months:
    month_data = statement_transactions_in(directory, month, year)
    new_data = pd.DataFrame(data=month_data[1:], columns=month_data[0])
    data = pd.concat([data, new_data], ignore_index=True)

  return data

def running_total(dataframe):
  trans_dates_amts = dataframe[["TRANS DATE", "AMT"]]
  total = 0
  totals = []

  for i, row in trans_dates_amts.iterrows():
    if(row["AMT"][-1]=="-"):
      val = row["AMT"][:-1]
      total -= float(val)
    else:
      total += float(row["AMT"])

    totals.append(total)

  return dataframe.assign(TOTAL=totals)

def save_df_to_csv(dataframe, filepath):
  dataframe.to_csv(filepath, index=False)


