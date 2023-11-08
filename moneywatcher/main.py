from calculate.totals import estatements_to_df, running_total_df, daily_totals_df
from calculate.expense_types import common_creditors_path, determine_creditor_type
from calculate.display import display_total_v_time, display_pie
from utils.df_csv import save_df_to_csv, load_csv_to_df, makedir, find_file, load_or_create_df
from utils.list_csv import load_csv_to_list, save_list_to_csv
from utils.date_time import get_first_last_date


###########################################################################################

def filename_prefix(year, months):
  if(len(months) == 1):
    return f"{year}_{months[0]}"
  elif(len(months) >= 2):
    return f"{year}_{months[0]}_to_{months[-1]}"
  else:
    return "Null_Null"


def squash_amts_by_creditors(data):
  creditors = data.groupby("WHO")["AMT"].sum()
  portions, labels = creditors.values, creditors.index
  return portions, labels

def squash_amts_by_expense_types(data):
  expense_types = data.groupby("expense_type")["AMT"].sum()
  portions, labels = expense_types.values, expense_types.index
  return portions, labels


def squash_amts_by_expense_subtypes(data):
  expense_subtypes = data.groupby(["expense_type", "expense_subtype"])["AMT"].sum()
  portions, labels = expense_subtypes.values, expense_subtypes.index.to_series().apply(lambda x: f"{x[0]} - {x[1]}")
  return portions, labels

###########################################################################################

def categorize_ind_month(year, months, data_directory):
  # Load E-Statements Data 
  prefix = filename_prefix(year, months)
  filename = prefix+"_estatement_transactions.csv"
  estatements_df = load_or_create_df(data_dir=data_directory, filename=filename, func=estatements_to_df, input_df=[months, year])
  
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
  creditor_portions, creditor_labels = squash_amts_by_creditors(creditor_types[["WHO", "AMT"]])
  expense_type_portions, expense_type_labels = squash_amts_by_expense_types(creditor_types[["expense_type", "AMT"]])
  expense_subtype_portions, expense_subtype_labels = squash_amts_by_expense_subtypes(creditor_types[["expense_subtype","expense_type", "AMT"]])

  # Display Monthly Portion of Expenses
  print("\n### DISPLAY DATA ###")
  display_pie(labels=creditor_labels, portions=creditor_portions, title=f"{first_date} to {last_date} -  Creditor $")
  display_pie(labels=expense_type_labels, portions=expense_type_portions, title=f"{first_date} to {last_date} -  Expense Types $")
  display_pie(labels=expense_subtype_labels, portions=expense_subtype_portions, title=f"{first_date} to {last_date} - Expense Subtypes $")

  ret = {
  "creditor_types":creditor_types,
  "first_date":first_date,
  "last_date":last_date,
  "creditors":[creditor_portions, creditor_labels],
  "expense_types":[expense_type_portions, expense_type_labels],
  "expense_subtypes":[expense_subtype_portions, expense_subtype_labels],
  }
  return ret
###########################################################################################
def main():

  # Input Data
  data_directory = "../data/"
  year = 2023
  months = [
    "January",
    # "February",
    # "March", 
    # "April",
    # "May", 
    # "June", 
    # "July", 
    # "August", 
    # "September", 
    # "October",
    # "November",
    ]
  data = categorize_ind_month(year, months, data_directory)
  #********************
  # filename = f"{year}_{months[0]}_to_{months[-1]}_daily_totals.csv"
  # daily_delta_df = load_or_create_df(data_dir=data_directory, filename=filename, func=daily_totals_df, estatements_df=estatements_df)
  # print(daily_delta_df)
  # Display Data #
  # display_total_v_time(totals_df)






###########################################################################################
if __name__ == '__main__':
  main()