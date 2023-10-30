from calculator.transform import estatements_to_df, running_total_df, daily_totals_df
from calculator.display import display_total_v_time
from utils.df_csv import save_df_to_csv, load_csv_to_df, makedir, find_file


def load_or_create_estatements_df(data_dir, months, year, filename):
  sub_dir = "tables/vsa/"
  
  file = find_file(data_dir, filename)

  if(not file):
    # Create csv data of estatements
    data = estatements_to_df(data_dir, months, year)
    dir_path = data_dir+sub_dir
    makedir(dir_path)
    save_df_to_csv(data, dir_path+filename)

  else:
    data = load_csv_to_df(file)

  return data

def load_or_create_df(data_dir, filename, func, estatements_df):
  sub_dir = "tables/"+func.__name__+"/"
  file = find_file(data_dir, filename)

  if(not file):
    # Create csv data of estatements
    data = func(estatements_df)
    dir_path = data_dir+sub_dir
    makedir(dir_path)
    save_df_to_csv(data, dir_path+filename)

  else:
    data = load_csv_to_df(file)

  return data

###########################################################################################
def main():

  data_directory = "../data/"
  year = 2023
  months = [
    "January","February","March", "April",
    "May" , "June", "July", "August", 
    "September","October"]

  # Load Data #
  filename = f"{year}_{months[0]}_to_{months[-1]}_estatement_transactions.csv"
  estatements_df = load_or_create_estatements_df(data_directory, months, year, filename)
  print("E-Statements loaded/created")
  

  # Operate on Data #
  filename = f"{year}_{months[0]}_to_{months[-1]}_estatement_transactions_running_totals.csv"
  totals_df = load_or_create_df(data_dir=data_directory, filename=filename, func=running_total_df, estatements_df=estatements_df)

  #********************
  filename = f"{year}_{months[0]}_to_{months[-1]}_daily_totals.csv"
  daily_delta_df = load_or_create_df(data_dir=data_directory, filename=filename, func=daily_totals_df, estatements_df=estatements_df)

  # Display Data #
  # display_total_v_time(daily_delta_df)






###########################################################################################
if __name__ == '__main__':
  main()