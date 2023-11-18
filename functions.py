import csv
import re
import os


def read_data_file(data_file):
    """Read the csv data file into a list of dictionaries"""
    data_list = []
    with open(data_file, encoding='utf-8-sig') as csv_file:
        data_dict = csv.DictReader(csv_file)
        for row in data_dict:
            data_list.append(dict(row))
    return data_list


def append_row_to_file(data_file, new_row):
    """Add a new transaction to the master expenses file"""
    fields = ['Date', 'Description', 'Amount', 'Transaction Type', 'Category', 'Account Name', 'Reference']
    with open(data_file, 'a', newline='') as csv_file:
        log_writer = csv.DictWriter(csv_file, fieldnames=fields)
        for item in new_row:
            log_writer.writerow(item)


def remove_extra_spaces(input_string):
    """Use a regular expression to replace two or more consecutive white spaces with a single space"""
    output_string = re.sub(r'\s{2,}', ' ', input_string)
    return output_string


def select_budget_category(categories_list):
    """Display a numbered list of budget categories and return selected category"""
    # Display numbered list and select
    print('Budget Categories: ')
    print('')
    n = 1
    for budget_category in categories_list:
        numbered_categories = f"{n}. {budget_category['Category']}"
        print(numbered_categories)
        n += 1
    print('')
    selected_category_num = int(input('Select Category Number: '))

    # Return selected category
    n = 1
    for budget_category in categories_list:
        if selected_category_num == n:
            return budget_category['Category']
        else:
            n += 1


def duplicate_check(master_list, new_transaction):
    """Read all transactions in the master list and determine if transaction already exists. Return keep or delete"""
    keep = True
    return keep


def build_amex_transactions(bank, transactions_list, categories_list, master_file):
    """Process AMEX transactions"""
    if bank == 'AMEX':
        for transaction in transactions_list:
            new_amex_transaction = []

            # Prep screen
            os.system('cls')
            print('')

            # Build new transaction
            date = transaction['Date']
            description = remove_extra_spaces(transaction['Description'])
            amount = float(transaction['Amount'])
            if amount <= 0:
                type = 'credit'
            else:
                type = 'debit'
            account_name = 'Blue Cash'
            reference = transaction['Reference']
            display_transaction = f"Date: {date}, Description: {description}, Amount: ${abs(amount)}\n"
            print(display_transaction)
            category = select_budget_category(categories_list)
            new_transaction = {'Date': date, 'Description': description, 'Amount': abs(amount), 'Transaction Type': type,
                               'Category': category, 'Account Name': account_name, 'Reference': reference}

            # Determine if transaction already exists
            transactions_master_list = read_data_file(master_file)
            keep = duplicate_check(transactions_master_list, new_transaction)

            # Append new transaction to master expenses list
            if keep:
                new_amex_transaction.append(new_transaction)
                append_row_to_file(master_file, new_amex_transaction)


def build_chase_transactions(bank, transactions_list, categories_list, master_file):
    """Process Chase transactions"""
    pass

