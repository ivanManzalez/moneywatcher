from calculate.totals import estatements_to_df, running_total_df, daily_totals_df
from calculate.expense_types import common_creditors_path, determine_creditor_type
from calculate.display import display_pie, plot_multilines
from utils.df_csv import save_df_to_csv, load_csv_to_df, makedir, find_file, load_or_create_df, concat_dataframes
from utils.list_csv import load_csv_to_list, save_list_to_csv
from utils.date_time import get_first_last_date
import pandas as pd
import matplotlib.pyplot as plt

###########################################################################################

def filename_prefix(year, months):
  if(len(months) == 1):
    return f"{year}_{months[0]}"
  elif(len(months) >= 2):
    return f"{year}_{months[0]}_to_{months[-1]}"
  else:
    return "Null_Null"

def squash_amts_by(column_names, data):
  return data.groupby(column_names)["AMT"].sum()

def portions_and_labels(categorized_data, multi_col=False):
  portions, labels = categorized_data.values, categorized_data.index
  
  if(multi_col):
    labels = labels.map(lambda x: '-'.join(map(str, x)))
  
  return portions, labels

def series_to_df(series_df):
  df_expenses = pd.DataFrame(series_df).transpose()
  return df_expenses.reset_index(drop=True)

###########################################################################################

def categorize_ind_month(year, months, data_directory):
  # Load E-Statements Data 
  prefix = filename_prefix(year, months)
  filename = prefix+"_estatement_transactions.csv"
  estatements_df = load_or_create_df(data_dir=data_directory, filename=filename, func=estatements_to_df, input_df=[data_directory, months, year])
  
  # Operate on Data #
  print("\n### E STATEMENT DATA ###")
  filename = prefix+"_estatement_transactions_running_totals.csv"
  totals_df = load_or_create_df(data_dir=data_directory, filename=filename, func=running_total_df, input_df=estatements_df)

  # Determine Creditor Types
  print("\n### CREDITOR TYPES DATA ###")
  data = totals_df[totals_df["AMT"]>0]
  filename = prefix+"_estatement_transaction_types.csv"
  creditor_types = load_or_create_df(data_dir=data_directory, filename=filename, func=determine_creditor_type, input_df=data)
  first_date, last_date = get_first_last_date(creditor_types)
  
  # Monthly Portion of Expenses
  print("\n### SQUASH DATA ###")
  creditors_series = squash_amts_by("WHO", creditor_types[["WHO", "AMT"]])
  creditors_series["End_Date"] = last_date
  
  expense_types_series = squash_amts_by("expense_type", creditor_types[["expense_type", "AMT"]])
  expense_types_series["End_Date"] = last_date
  
  expense_subtypes_series = squash_amts_by(["expense_type","expense_subtype"], creditor_types[["expense_type","expense_subtype", "AMT"]])
  expense_subtypes_series["End_Date"] = last_date
  
  creditors_df = series_to_df(creditors_series)
  expense_types_df = series_to_df(expense_types_series)
  expense_subtypes_df = series_to_df(expense_subtypes_series)


  # Display Monthly Portion of Expenses
  # print("\n### DISPLAY DATA ###")
  # display_pie(labels=creditor_labels, portions=creditor_portions, title=f"{first_date} to {last_date[4:]} -  Creditor $")
  # display_pie(labels=expense_type_labels, portions=expense_type_portions, title=f"{first_date} to {last_date[4:]} -  Expense Types $")
  # display_pie(labels=expense_subtype_labels, portions=expense_subtype_portions, title=f"{first_date} to {last_date[4:]} - Expense Subtypes $")


  return {
    # "first_date":first_date, #needed?
    "last_date":last_date,
    "creditors": creditors_df,
    "expense_types": expense_types_df,
    "expense_subtypes": expense_subtypes_df,
    }

###########################################################################################
def main():
  empty_df = pd.DataFrame(columns=[])
  # Input Data
  data_directory = "../data/"
  year = 2023
  months = [
    "January",
    "February",
    "March", 
    "April",
    "May", 
    "June", 
    "July", 
    "August", 
    "September", 
    "October",
    "November",
    ]

  last_dates = []
  creditors = empty_df
  expense_types = empty_df
  expense_subtypes = empty_df

  for month in months:
    result = categorize_ind_month(year, [month], data_directory)
    creditors = pd.concat([creditors, result["creditors"]], ignore_index=True)
    expense_types = pd.concat([expense_types, result["expense_types"]], ignore_index=True)
    expense_subtypes = pd.concat([expense_subtypes, result["expense_subtypes"]], ignore_index=True)
  

  creditors.fillna(0, inplace=True)
  expense_types.fillna(0, inplace=True)
  expense_subtypes.fillna(0, inplace=True)

  # Get Columns
  column_names = creditors.columns.tolist()
  expense_type_cols = expense_types.columns.tolist()
  expense_subtype_cols = expense_subtypes.columns.tolist()


  #********************
  print("\n### PLOTTING ###")
  first_date = expense_types["End_Date"].iloc[0]
  last_date = expense_types["End_Date"].iloc[-1]
  title_post = f"{first_date} to {last_date}"

  t = pd.to_datetime(expense_types["End_Date"], format='%Y %b. %d')
  t = t.dt.strftime('%y/%m/%d')


  # for col_name in expense_type_cols:

  #   if(col_name == "End_Date"):
  #     continue
    
  #   expense_subtype_cols = expense_subtypes[col_name].columns.tolist()

  #   plt.plot(t, expense_types[col_name], label=f"Total {col_name}",linewidth=1.5)
    
  #   for col_subname in expense_subtype_cols:
  #     plt.plot(t, expense_subtypes[col_name][col_subname], label=col_subname, linestyle='--')

  #   # Add labels and legend
  #   plt.xlabel('End Dates')
  #   plt.ylabel(f"CAD$ Spent on {col_name}")
  #   plt.title(f"{col_name.upper()}: {title_post}")
  #   plt.legend()
  #   plt.grid()

  #   plt.show()
  plt.figure(figsize=(15, 5))
  for col_name in expense_type_cols:
    if(col_name == "End_Date"):
      continue
    plt.plot(t, expense_types[col_name], label=f"{col_name}",linewidth=1.0)
  # Add labels and legend
  plt.xlabel('End Dates')
  plt.ylabel("Total CAD$")
  # plt.subplots_adjust(left=0.1)
  plt.subplots_adjust(right=0.8) 
  plt.title(f"Total Expenses: {title_post}")
  plt.legend(loc='center left', bbox_to_anchor=(1.0, 0.5))
  plt.grid()

  plt.show()
    



  #********************
  # filename = f"{year}_{months[0]}_to_{months[-1]}_daily_totals.csv"
  # daily_delta_df = load_or_create_df(data_dir=data_directory, filename=filename, func=daily_totals_df, estatements_df=estatements_df)
  # print(daily_delta_df)
  # Display Data #
  # display_total_v_time(totals_df)






###########################################################################################
if __name__ == '__main__':
  main()