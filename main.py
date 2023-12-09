from pathlib import Path
from tkinter import filedialog
from functions import *

#  Read Categories and Master Transactions files
categories_file = Path.home() / 'OneDrive' / 'Expense Tracker' / 'expense_categories.csv'
transactions_master_file = Path.home() / 'OneDrive' / 'Expense Tracker' / 'expenses_master.csv'
categories_list = read_data_file(categories_file)
transactions_master_list = read_data_file(transactions_master_file)

# Read new expenses from AMEX or Chase downloads
new_transactions_file = filedialog.askopenfilename(initialdir=Path.home() / 'OneDrive' / 'Downloads',
                                                   title='Select new transactions export file',
                                                   filetypes=(('csv files', '*.csv'), ('all files', '*.*')))

new_transactions_list = read_data_file(new_transactions_file)


# Determine if expenses are from AMEX or Chase and call appropriate function
if 'Reference' in new_transactions_list[0].keys():
    bank = 'AMEX'
    build_amex_transactions(bank, new_transactions_list, categories_list, transactions_master_file)
else:
    bank = 'Chase'
    build_chase_transactions(bank, new_transactions_list, categories_list, transactions_master_file)
