from utils.list_csv import load_csv_to_list, save_list_to_csv

def expenses():
  return [
    ("Food",["Fast", "Groceries", "Experience", "Liqs"]),
    ("Transportation",["Gasoline", "Public Transit", "Uber", "Parking", "Maintenance"]),
    ("Utilities",["Housing", "Phone", "Storage", "Cleaning Supplies", "Insurance"]),
    ("Entertainment",["Video Streaming", "Music", "Event", "Game", "Art"]),
    ("Clothing",["Business", "Casual"]),
    ("Education",["Books", "Tuition"]),
    ("Medical",["Session", "Equipment", "Medication"]),
    ("Miscellaneous",["Unknown", "Gift"]),
  ]

common_creditors_path = "../data/tables/common_creditors.csv"
COMMON_CREDITORS = load_csv_to_list(common_creditors_path)

################################################################################

def display_expense_type(EXPENSES):
  
  # Show all options to user
  print("\n(", end=" ")
  for i in range(len(EXPENSES)):
    print(f"{i} - {EXPENSES[i][0]} |", end=" ")
  print(")")

  # Validate User Input
  expense_type = str(input("\nPlease Enter Expense type (or new): "))

  if(expense_type.lower() == "new"):
    new_expense_type = str(input("\nPlease Enter a NEW Expense type: "))
    EXPENSES.append((new_expense_type, []))
    EXPENSES, expense_type = display_expense_type(EXPENSES)
  expense_type = str(expense_type)

  if(not expense_type.isnumeric()):
    print("Input must be numeric")
    EXPENSES, expense_type = display_expense_type(EXPENSES)
  
  expense_type = str(expense_type)

  # Validate Expense Type
  if(int(expense_type) >= len(EXPENSES)):
    print("Invalid type")
    EXPENSES, expense_type = display_expense_type(EXPENSES)

  return EXPENSES, int(expense_type)

################################################################################################

def display_expense_subtype(expense_type, EXPENSES):
  
  # Add new subtype
  if(len(EXPENSES[expense_type][1]) == 0):
    new_expense_subtype = str(input(f"\nPlease Enter a new {EXPENSES[expense_type][0]} subtype: "))
    EXPENSES[expense_type][1].append(new_expense_subtype)

  # Show all options to user
  print("\n(", end=" ")
  for i in range(len(EXPENSES[expense_type][1])):
    print(f"{i} - {EXPENSES[expense_type][1][i]} |", end=" ")
  print(")")

  # Validate User Input
  expense_subtype = str(input("\nPlease Enter Expense subtype (or new): "))

  if(expense_subtype.lower() == "new"):
    new_expense_subtype = str(input("\nPlease Enter a NEW Expense subtype: "))
    EXPENSES[expense_type][1].append(new_expense_subtype)
    EXPENSES, expense_subtype = display_expense_subtype(expense_type, EXPENSES)
  expense_subtype = str(expense_subtype)

  if(not expense_subtype.isnumeric()):
    print("Input must be numeric")
    EXPENSES, expense_subtype = display_expense_subtype(expense_type, EXPENSES)
  expense_subtype = str(expense_subtype)

  # Validate Expense Subtype
  if(int(expense_subtype) >= len(EXPENSES[expense_type][1])):
    print("Invalid Subtype")
    EXPENSES, expense_subtype = display_expense_subtype(expense_type, EXPENSES)
  
  return EXPENSES, int(expense_subtype)

################################################################################################

def display_common_creditors(creditor_name):
  common_creditors = []
  print("")
  for i in range(len(COMMON_CREDITORS)):

    if(COMMON_CREDITORS[i][0].lower() in creditor_name.lower()):
      print(f"{i} - {COMMON_CREDITORS[i][0]} ({COMMON_CREDITORS[i][1]}/{COMMON_CREDITORS[i][2]}) ")
      common_creditors.append(i)
  N = len(common_creditors)
  if(N<1):
    print("No common Creditors.")
    for i in range(len(COMMON_CREDITORS)):
      print(f"{i} - {COMMON_CREDITORS[i][0]} ({COMMON_CREDITORS[i][1]}/{COMMON_CREDITORS[i][2]}) ")
    print("")
    common_creditors = creditor_name
  
  return N, common_creditors
################################################################################################

def determine_creditor_type(creditors):
  EXPENSES = expenses()
  N = creditors.shape[0]
  counter = 0
  expense_type_list = []
  expense_subtype_list = []

  for i,data in creditors.iterrows():
    counter += 1
    creditor_name = creditors.loc[i, 'WHO']
    transaction_amt = creditors.loc[i, 'AMT']
    transaction_date = creditors.loc[i, 'TRANS DATE']
    
    print("===========================================\n===========================================")
    print(f"\n({counter}/{N}) CREDITOR : {creditor_name} $ {transaction_amt} on {transaction_date}")
    
    num_suggestions, suggested = display_common_creditors(creditor_name)
    new_name = str(input(f"Input Existing ID or New Creditor Name ({suggested}): "))
    
    if(num_suggestions == 0 and new_name == ""):
      new_name = creditor_name
      
    if(num_suggestions == 1 and new_name == ""):
      new_name = suggested[0]

    if(num_suggestions > 1):
      while(new_name == ""):
        new_name = str(input(f"Input Existing ID or New Creditor Name ({suggested}): "))

    if(str(new_name).isnumeric()):
      new_name = int(new_name)
      name = COMMON_CREDITORS[new_name][0]
      expense_type = COMMON_CREDITORS[new_name][1]
      expense_subtype = COMMON_CREDITORS[new_name][2]
      
      creditors.loc[i, 'WHO'] = name.upper()
      expense_type_list.append(expense_type)
      expense_subtype_list.append(expense_subtype)
      print(f"{name} Recorded as {expense_type}|{expense_subtype}")
      continue

    creditors.loc[i, 'WHO'] = new_name.upper()
    print(f"\nCREDITOR : {creditors.loc[i, 'WHO']} $ {float(creditors.loc[i, 'AMT'])} on {creditors.loc[i, 'TRANS DATE']}")
    
    EXPENSES, expense_type = display_expense_type(EXPENSES)
    EXPENSES, expense_subtype = display_expense_subtype(expense_type , EXPENSES)

    COMMON_CREDITORS.append([new_name.upper(), EXPENSES[expense_type][0], EXPENSES[expense_type][1][expense_subtype]])
    expense_type_list.append(EXPENSES[expense_type][0])
    expense_subtype_list.append(EXPENSES[expense_type][1][expense_subtype])
    print(f"{new_name} Recorded as {EXPENSES[expense_type][0]}|{EXPENSES[expense_type][1][expense_subtype]}")
  
  save_list_to_csv(COMMON_CREDITORS, common_creditors_path)
  creditors["expense_type"] = expense_type_list
  creditors["expense_subtype"] = expense_subtype_list
  
  print(creditors)
  return creditors 
