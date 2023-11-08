import csv

def load_csv_to_list(filepath):
  data = []
  with open(filepath, "r") as file:
    csv_reader = csv.reader(file, quoting=csv.QUOTE_NONE)
    for row in csv_reader:
      cleaned_row = [value.strip('"') for value in row]
      data.append(cleaned_row)
  return data

def save_list_to_csv(list_data, filepath):

  with open(filepath, "w", newline="\n") as file:
    csv_writer = csv.writer(file, quoting=csv.QUOTE_NONE)
    for row in list_data:
      csv_writer.writerow(row)

  print(f"Successfully saved {filepath}")