from statement_reader.vsa_statement_reader import statement_transactions_in
from utils.date_time import days_in_year,Mmm_Dd_YYYY_to_YYYY_MM_DD
import pandas as pd

############################################################################################################

def clean_dates(month, year, dataframe, date_field):
  new_dates = []
  dates = dataframe[date_field]
 
  for date in dates:
    if ("Dec" in date):
      new_date = date +" "+ str(year-1)

    else:
      new_date = date +" "+ str(year)

    new_date = Mmm_Dd_YYYY_to_YYYY_MM_DD(new_date)
    new_dates.append(new_date)

  dataframe.loc[:, date_field] = new_dates

  return dataframe

def clean_negatives(dataframe, number_field):
  new_numbers = []
  values = dataframe[number_field]
 
  for value in values:
    if (value[-1]=="-"):
      new_number = -float(value[:-1])

    else:
      new_number = float(value)

    new_numbers.append(new_number)

  dataframe.loc[:, number_field] = new_numbers

  return dataframe

# Transform Scotia VISA E Statements to Pandas df 
def estatements_to_df(inputs):
  directory = inputs[0]
  months    = inputs[1]
  year      = inputs[2]
  data = pd.DataFrame()
  
  for month in months:
    month_data = statement_transactions_in(directory, month, year)
    new_data = pd.DataFrame(data=month_data[1:], columns=month_data[0])
    new_data = clean_dates(month, year, new_data, "TRANS DATE")
    new_data = clean_dates(month, year, new_data, "POSTED DATE")
    new_data = clean_negatives(new_data, "AMT")
    data = pd.concat([data, new_data], ignore_index=True)
  return data

# Using E Statements df Calculate Running Total after each Transaction
def running_total_df(dataframe):
  trans_dates_amts = dataframe[["TRANS DATE", "AMT"]]
  total = 0
  totals = []

  for i, row in trans_dates_amts.iterrows():
    total += float(row["AMT"])
    totals.append(total)

  return dataframe.assign(TOTAL=totals)

# Using E Statements df Squash Same Date to 1 record and 1 final total
def daily_totals_df(dataframe):
  dates = dataframe["TRANS DATE"].drop_duplicates().tolist()
  dates.sort(reverse=False)

  daily_totals = []
  running_total = 0

  for date in dates:
    dates_data = dataframe[dataframe["TRANS DATE"] == date]
    daily_total=0
    for i, row in dates_data.iterrows():
      daily_total += row["AMT"]

    running_total+= daily_total
    daily_totals.append([date, running_total, daily_total])

  data = pd.DataFrame(data=daily_totals, columns=["TRANS DATE", "RUNNING_TOTAL", "TOTAL_DELTA"])
  
  return data











