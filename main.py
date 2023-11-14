import csv
from pathlib import Path
from tkinter import filedialog


def read_data_file(data_file):
    """Read the csv data file into a list of dictionaries"""
    data_list = []
    with open(data_file, encoding='utf-8-sig') as csv_file:
        data_dict = csv.DictReader(csv_file)
        for row in data_dict:
            data_list.append(dict(row))
    return data_list


#  Read Expense Categories and Master Expenses files
expense_categories_file = Path.home() / 'OneDrive' / 'Expense Tracker' / 'expense_categories.csv'
expenses_master_file = Path.home() / 'OneDrive' / 'Expense Tracker' / 'expenses_master.csv'
expense_categories_list = read_data_file(expense_categories_file)
expenses_master_list = read_data_file(expenses_master_file)

# Read new expenses from AMEX or Chase downloads
new_expenses_file = filedialog.askopenfilename(initialdir=Path.home() / 'OneDrive' / 'Downloads',
                                               title='Select new expenses export file',
                                               filetypes=(('csv files', '*.csv'), ('all files', '*.*')))

new_expenses_list = read_data_file(new_expenses_file)

print(new_expenses_list)
