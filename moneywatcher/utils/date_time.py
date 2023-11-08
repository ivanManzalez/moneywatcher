from datetime import datetime, date, timedelta
import pandas as pd


def days_in_year(year):
  first_day = date(year, 1, 1)
  last_day = date(year, 12, 31)

  num_days = (last_day - first_day).days + 1

  return num_days

def Mmm_Dd_YYYY_to_YYYY_MM_DD(datestring):
  original_date = datetime.strptime(datestring, "%b %d %Y")
  return original_date.strftime("%Y-%m-%d")

   
def get_first_last_date(df):
  # Convert the 'TRANS DATE' column to a datetime format
  df['TRANS DATE'] = pd.to_datetime(df['TRANS DATE'])

  # Sort the DataFrame by 'TRANS DATE' in ascending order
  df.sort_values(by='TRANS DATE', inplace=True)

  # Get the first and last 'TRANS DATE' values
  first_date = df.iloc[0]['TRANS DATE'].strftime("%Y %b. %d")
  last_date = df.iloc[-1]['TRANS DATE'].strftime("%b. %d")
  return first_date, last_date