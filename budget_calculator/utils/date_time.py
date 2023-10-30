from datetime import datetime, date, timedelta


def days_in_year(year):
  first_day = date(year, 1, 1)
  last_day = date(year, 12, 31)

  num_days = (last_day - first_day).days + 1

  return num_days

def Mmm_Dd_YYYY_to_YYYY_MM_DD(datestring):
  original_date = datetime.strptime(datestring, "%b %d %Y")
  return original_date.strftime("%Y-%m-%d")

   
