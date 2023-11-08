import pandas as pd
import os

################################################################
def save_df_to_csv(dataframe, filepath):
  dataframe.to_csv(filepath, index=False)

def load_csv_to_df(filepath):
  return pd.read_csv(filepath)

def makedir(directory_path):
  if not os.path.exists(directory_path):
    os.makedirs(directory_path)

def find_file(start_directory, filename):
  for root, dirs, files in os.walk(start_directory):

    if (filename in files):
      file_path = os.path.join(root, filename)
      file_found = True
      print("File found:", file_path)
      return file_path

    for sub_dir in dirs:
      result = find_file(os.path.join(root, sub_dir), filename)
      if result:
        return result
      
  # print(f"The file '{filename}' was not found in any directory under '{start_directory}'.")
  return None

def load_or_create_df(data_dir, filename, func, input_df):
  
  sub_dir = "tables/"+func.__name__+"/"

  if(func.__name__=="estatements_to_df"):
    sub_dir = "tables/vsa/"
  

  file = find_file(data_dir, filename)
  print("FILE:",file)
  if(not file):
    # Create csv data 
    print("Create csv tables input dataframe ")
    data = func(input_df)
    dir_path = data_dir+sub_dir
    makedir(dir_path)
    save_df_to_csv(data, dir_path+filename)

  else:
    print("Load data")
    data = load_csv_to_df(file)

  return data