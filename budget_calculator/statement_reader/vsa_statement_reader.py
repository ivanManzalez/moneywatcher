import PyPDF2 
from logger.logger import Logger
from logger.log_configs import DEBUG, LOG_FORMAT
from datetime import datetime
import os
######################################################################
date = datetime.now().strftime("%Y-%m-%d.log")
directory_path = f"./logger/logs/"

if not os.path.exists(directory_path):
      os.makedirs(directory_path)

vsa = Logger(__name__, DEBUG)
vsa.set_handler(directory_path+date, LOG_FORMAT)
 
######################################################################
def find(target_value, transactions):
  # print(f"--find ({target_value})--")
  vsa.logger.info(f"Look for {target_value}")
  ret = []

  for i, value in enumerate(transactions):
    if value == target_value:
      vsa.logger.info(f"Match @ {i}")
      ret.append(i)
      return ret

  return ret

######################################################################
def find_payment(transactions):
  target_value = "MB-CREDIT CARD/LOC PAY."
  return find(target_value, transactions)

def clean_payment_entry(payment_indexes, transactions):
  # print("--clean_payment_entry--", payment_indexes)
  vsa.logger.info(f"{payment_indexes}")
  while(payment_indexes):
    index = payment_indexes[0]
    # print("Payment:", transactions[index:index+7], index)
    vsa.logger.info(f"{transactions[index:index+7]} @ {index}")
    # 
    for i in range(1,7):
      if i < 4:
        transactions[index] += transactions[index+1]
        transactions.pop(index+1) 
      if i == 4:
        transactions.insert(index+1,"Payment")
      if i == 5:
        transactions.insert(index+2,"Payment")
      if i == 6:
        if (transactions[index+4] == "-"):
          transactions[index+3] += transactions[index+4]
          transactions.pop(index+4)
    # 
    payment_indexes.pop(0)
    next_payment_trans = find_payment(transactions[index+6:])
    
    if(next_payment_trans):
      # print(index+6 + next_payment_trans[0])
      payment_indexes.append(index+6 + next_payment_trans[0])

  
  return transactions

######################################################################
def find_boardgamearena(transactions):
  target_value = "BOARDGAMEARENA"
  return find(target_value, transactions)

def clean_boardgamearena_entry(bga_indexes, transactions):
  vsa.logger.info(f"{bga_indexes}")
  for index in bga_indexes:
    transactions.insert(index+2,"FRANCE")
  return transactions
######################################################################
def find_usd_purchase(transactions):
  target_value = "ED STATES DOL" #ED STATES DOL

  return find(target_value, transactions)

def clean_usdpurchase_entry(usdpurch_indexes, transactions):
  vsa.logger.info(f"{usdpurch_indexes}")
  while usdpurch_indexes:
    # print("usdpurch_indexes:",usdpurch_indexes)
    index = usdpurch_indexes.pop(0)
    transactions.pop(index-2) # AMT
    transactions.pop(index-2) # $ UNIT
    transactions.pop(index-2) # ED STATES DOL
    transactions.pop(index-2) # LAR

    next_usd_trans = find_usd_purchase(transactions[index+1:])
    
    if(next_usd_trans):
      usdpurch_indexes.append(index+1 + next_usd_trans[0])

  return transactions

######################################################################
def find_mountainview(transactions):
  target_value = "MOUNTAIN VIEW" 
  return find(target_value, transactions)

def clean_mntview(city_indexes, transactions):
  vsa.logger.info(f"{city_indexes}")

  while city_indexes:
    index = city_indexes.pop(0)
    
    if (transactions[index+1] != "CA"):
      transactions.insert(index+1, "CA")

    next_mntvw = find_mountainview(transactions[index+1:])
    
    if(next_mntvw):
      city_indexes.append(index+1 + next_mntvw[0])

  return transactions



def find_santaclara(transactions):
  target_value = "SANTA CLARA"
  return find(target_value, transactions)

def clean_santaclara(city_indexes, transactions):
  vsa.logger.info(f"{city_indexes}")

  while city_indexes:
    index = city_indexes.pop(0)
    
    if (transactions[index+1] != "CA"):
      transactions.insert(index+1, "CA")

    next_santaclara = find_santaclara(transactions[index+1:])
    
    if(next_santaclara):
      city_indexes.append(index+1 + next_santaclara[0])
  return transactions


def find_denver(transactions):
  target_value = "DENVER"
  return find(target_value, transactions)

def clean_denver(city_indexes, transactions):
  vsa.logger.info(f"{city_indexes}")

  while city_indexes:
    index = city_indexes.pop(0)
    
    if (transactions[index+1] != "CO"):
      transactions.insert(index+1, "CO")

    next_denver = find_denver(transactions[index+1:])
    
    if(next_denver):
      city_indexes.append(index+1 + next_denver[0])
  return transactions

######################################################################
def find_applepay(transactions):
  target_value = "(APPLE" 
  return find(target_value, transactions)

def clean_applepay(apple_pay_indexes, transactions):
  vsa.logger.info(f"{apple_pay_indexes}")

  while apple_pay_indexes:
    index = apple_pay_indexes.pop(0)
    
    if (transactions[index+1] == "PAY)"):
      transactions.pop(index)
      transactions.pop(index)

    next_applepay = find_applepay(transactions[index:])
    
    if(next_applepay):
      apple_pay_indexes.append(index + next_applepay[0])

  return transactions

######################################################################
def find_creditvoucher(transactions):
  target_value = "CREDIT VOUCHER/RETURN" 
  return find(target_value, transactions)

def clean_creditvoucher(voucher_indexes, transactions):
  vsa.logger.info(f"{voucher_indexes}")

  while voucher_indexes:
    index = voucher_indexes.pop(0)
    
    transactions[index+4] += transactions[index+5]
    
    transactions.pop(index+5)
    transactions.pop(index)

    next_voucher = find_applepay(transactions[index:])
    
    if(next_voucher):
      voucher_indexes.append(index + next_voucher[0])

  return transactions

######################################################################
def create_transactions_table(transactions):
  vsa.logger.info(f"")
  transaction_table = []
  row = []

  ### Credit Card Payments ###
  payment_indexes = find_payment(transactions)
  if(payment_indexes):
    transactions = clean_payment_entry([payment_indexes[0]], transactions)

  ### One type payments ###
  bga_indexes = find_boardgamearena(transactions)
  transactions = clean_boardgamearena_entry(bga_indexes, transactions)

  ### USD Transactions ###
  usdpurch_indexes = find_usd_purchase(transactions)
  if(usdpurch_indexes):
    transactions = clean_usdpurchase_entry([usdpurch_indexes[0]], transactions)
  
  ### How to refactor: Clean American City/State ###
  mntvw_indexes = find_mountainview(transactions)
  if(mntvw_indexes):
    transactions = clean_mntview([mntvw_indexes[0]], transactions)

  santaclara_indexes = find_santaclara(transactions)
  if(santaclara_indexes):
    transactions = clean_santaclara([santaclara_indexes[0]], transactions)

  denver_indexes = find_denver(transactions)
  if(denver_indexes):
    transactions = clean_denver([denver_indexes[0]], transactions)

  ### Apple Pay ###
  apple_pay_indexes = find_applepay(transactions)
  if(apple_pay_indexes):
    transactions = clean_applepay([apple_pay_indexes[0]], transactions)

  ### Plato's Closet Return Voucher ###
  voucher_indexes = find_creditvoucher(transactions)
  if(voucher_indexes):
    transactions = clean_creditvoucher([voucher_indexes[0]], transactions)

  ########################

  for i in range(len(transactions)):
    if(i%7 == 0): # trans. number
      row.append(transactions[i])

    if(i%7 == 1): # trans. date
      row.append(transactions[i])

    if(i%7 == 2): # post date
      row.append(transactions[i])

    if(i%7 == 3): # Store
      row.append(transactions[i])

    if(i%7 == 4): # City
      row.append(transactions[i])

    if(i%7 == 5): # Province
      row.append(transactions[i])

    if(i%7 == 6): # Amount ($)
      row.append(transactions[i])
      transaction_table.append(row)
      row = []

  return transaction_table

######################################################################
def tabulate_scotiabank_estatement(filepath):
  reader = PyPDF2.PdfReader(filepath)
  statement_transactions = [['TRANSACTION #', 'TRANS DATE', 'POSTED DATE', 'WHO', 'CITY', 'PROV/STATE', 'AMT']]
  # print("# of pages",len(reader.pages))
  vsa.logger.info(f"Number of pages {len(reader.pages)}")
  for page in range(len(reader.pages)):
    # print(f"\n\n--- Page#{page} ---")
    vsa.logger.info(f"Page#{page}")

    statement_string = reader.pages[page].extract_text()
    words = statement_string.split("\n")
    
    if("Transactions since your last statement" in words):
      table_start = find("Transactions since your last statement", words)[0]
      table_end = find("If you have any questions about this", words)[0]
      
      transactions_start = table_start + 12 # found manually
      transactions_end = table_end
      transactions = words[transactions_start : transactions_end]
      
      statement_transactions = statement_transactions+create_transactions_table(transactions)

    elif("Transactions - continued" in words):
      table_start = find("Transactions - continued", words)[0]
      table_end = find("SUB-TOTAL CREDITS", words)
      if(not table_end):
        table_end = find("SBVREP_10100_D23121_A - 0037233    HRI - - 2 - 2 - 27 - 4-    132151", words)

      transactions_start = table_start + 8 # found manually
      transactions_end = table_end[0]
      transactions = words[transactions_start : transactions_end] 
      
      statement_transactions = statement_transactions+create_transactions_table(transactions)

    else:
      vsa.logger.info(f"Does not contain a transactions table")
      # print("Does not contain a transactions table")
  return statement_transactions


######################################################################

def statement_transactions_in(directory, month, year):

  path = directory + f"/visa/{year}/"
  file = f"{month}{year}_e-Statement.pdf"
  statement_transactions = tabulate_scotiabank_estatement(path+file)
  return statement_transactions
######################################################################



