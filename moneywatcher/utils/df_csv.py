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
################################################################
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

################################################################
def concat_dataframes(df1, df2):
  # Step 1: Identify unique column names from both DataFrames
  columns_df1 = set(df1.columns)
  columns_df2 = set(df2.columns)

  if(columns_df1 == columns_df2):
    return pd.concat([df1, df2], ignore_index = True)

  # Step 2: Create a new DataFrame with the union of unique column names
  all_columns = list(columns_df1.union(columns_df2))
  merged_df = pd.DataFrame(columns=all_columns)

  # Step 3: Fill missing columns in each original DataFrame with 0s
  for column in all_columns:
    if column not in columns_df1:
      df1[column] = 0
    if column not in columns_df2:
      df2[column] = 0

  # Step 4: Concatenate the modified DataFrames
  result_df = pd.concat([df1, df2], ignore_index=True)

  return result_df