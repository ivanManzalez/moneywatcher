from calculator.transform import estatements_to_df, running_total
from utils.df_csv import save_df_to_csv, load_csv_to_df
import os

def makedir(directory_path):
  if not os.path.exists(directory_path):
    os.makedirs(directory_path)

def find_file(start_directory, filename):
  for root, dirs, files in os.walk(start_directory):

    if (filename in files):
      file_path = os.path.join(root, filename)
      file_found = True
      return file_path

    for sub_dir in dirs:
      result = find_file(os.path.join(root, sub_dir), filename)
      if result:
        return result
      
  print(f"The file '{filename}' was not found in any directory under '{start_directory}'.")
  return None

def load_or_create(data_dir, months, year):
  sub_dir = "tables/amounts/"
  filename = "estatement_data_total_balance.csv"
  file = find_file(data_dir, filename)

  if(not file):
    # Create csv data of estatements
    estatements_df = estatements_to_df(data_dir, months, year)
    data = running_total(estatements_df)
    dir_path = data_dir+sub_dir
    makedir(dir_path)
    save_df_to_csv(data, dir_path+filename)
  
  else:
    data = load_csv_to_df(file)

  return data

###########################################################################################
def main():
  directory = "../data"
  year = 2023
  months = [
    "January","February","March", "April",
    "May" , "June", "July", "August", 
    "September","October"]

  data = load_or_create(directory, months, year)
  print(data)
  

if __name__ == '__main__':
  main()