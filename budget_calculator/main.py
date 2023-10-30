from calculator.transform import estatements_to_df, running_total, save_df_to_csv
import os

def makedir(directory_path):
  if not os.path.exists(directory_path):
    os.makedirs(directory_path)

def find_file(start_directory, filename):
  file_found = False

  for root, dirs, files in os.walk(start_directory):
    print(root, dirs, files)
    if filename in files:
      file_path = os.path.join(root, filename)
      print(f"File found @ {file_path}")
      return file_path

    else:
      print(f"The file '{filename}' was not found in any directory under '{start_directory}'.")
      return None

###########################################################################################
def main():
  directory = "../data/"
  year = 2023
  months = [
    "January","February","March", "April",
    "May" , "June", "July", "August", 
    "September","October"]

  #
  sub_dir = "tables/amounts/"
  filename = "estatement_data_total_balance.csv"
  file = find_file(directory, sub_dir+filename)
  
  if(not file):
    print("create")
    # Create csv data of estatements
    data = estatements_to_df(directory, months, year)
    data_with_total = running_total(data)

    dir_path = directory+sub_dir
    makedir(dir_path)
    save_df_to_csv(data_with_total, dir_path+filename)
  
  else:
    print("load")
    data = load_estatement_tables(file)

  print(data)
  

if __name__ == '__main__':
  main()