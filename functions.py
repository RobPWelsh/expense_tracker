import csv
import re
import os
import colorama
from colorama import Fore

colorama.init(autoreset=True)


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
    print('Budget Categories:\n')
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


def duplicate_check(bank, master_list, new_transaction):
    """Read all transactions in the master list and determine if transaction already exists. Return keep or delete"""
    keep = True
    decision_message = f"{Fore.RED}Transaction already exists! Keep transaction (Y/N): "
    for transaction in master_list:
        if bank == 'AMEX' and transaction['Reference'] == new_transaction['Reference']:
            keep_decision = input(decision_message).lower()
            if keep_decision == 'y':
                keep = True
            else:
                keep = False
            return keep
        elif (bank == 'Chase' and transaction['Date'] == new_transaction['Date'] and transaction['Description'] ==
              new_transaction['Description']):
            keep_decision = input(decision_message).lower()
            if keep_decision == 'y':
                keep = True
            else:
                keep = False
            return keep
    return keep


def build_amex_transactions(bank, transactions_list, categories_list, master_file):
    """Process AMEX transactions"""
    for transaction in transactions_list:
        new_amex_transaction = []

        # Prep screen
        os.system('cls')
        print('')

        # Build new transaction
        date = transaction['Date']
        description = remove_extra_spaces(transaction['Description'])
        amount = float(transaction['Amount'])

        # invert amount
        amount = amount * -1

        if amount <= 0:
            type = 'debit'
        else:
            type = 'credit'

        account_name = 'American Express'
        reference = transaction['Reference']
        display_transaction = f"Date: {date}, Description: {description}, Amount: ${amount}, Type: {type}\n"
        print(display_transaction)
        category = select_budget_category(categories_list)
        new_transaction = {'Date': date, 'Description': description, 'Amount': amount, 'Transaction Type': type,
                           'Category': category, 'Account Name': account_name, 'Reference': reference}

        # Determine if transaction already exists
        transactions_master_list = read_data_file(master_file)
        keep = duplicate_check(bank, transactions_master_list, new_transaction)

        # Append new transaction to master expenses list if not duplicate
        if keep:
            new_amex_transaction.append(new_transaction)
            append_row_to_file(master_file, new_amex_transaction)


def build_chase_transactions(bank, transactions_list, categories_list, master_file):
    """Process Chase transactions"""
    for transaction in transactions_list:
        new_chase_transaction = []

        # Prep screen
        os.system('cls')
        print('')

        # Build new transaction
        date = transaction['Posting Date']
        description = remove_extra_spaces(transaction['Description'])

        amount = float(transaction['Amount'])
        if amount >= 0:
            type = 'credit'
        else:
            type = 'debit'
        account_name = 'Chase Checking'

        reference = ''
        display_transaction = f"Date: {date}, Description: {description}, Amount: ${amount}, Type: {type}\n"
        print(display_transaction)
        category = select_budget_category(categories_list)
        new_transaction = {'Date': date, 'Description': description, 'Amount': amount, 'Transaction Type': type,
                           'Category': category, 'Account Name': account_name, 'Reference': reference}

        # Determine if transaction already exists
        transactions_master_list = read_data_file(master_file)
        keep = duplicate_check(bank, transactions_master_list, new_transaction)

        # Manage insurance and internet payments if needed.
        # Append new transaction to master expenses list if not duplicate
        if keep:
            if 'LAKE SHORE CRYOT PAYROLL' in new_transaction['Description']:

                # Create a new transaction for the insurance and append it to the expenses master file
                add_insurance = input('Transaction is Lake Shore pay. Split to add insurance (Y/N): ').lower()
                if add_insurance == 'y':
                    insurance_amt = float(input('Enter insurance amount (typical = 103.40): '))
                    insurance_amt = insurance_amt * -1
                    new_insurance_transaction = {'Date': date, 'Description': 'Liberty Mutual Insurance',
                                                 'Amount': insurance_amt, 'Transaction Type': 'debit',
                                                 'Category': 'Insurance - Auto, Home, Umbrella',
                                                 'Account Name': account_name, 'Reference': reference}
                    new_chase_transaction.append(new_insurance_transaction)
                    append_row_to_file(master_file, new_chase_transaction)
                    new_chase_transaction = []

                    # Add the insurance amount to the paycheck transaction
                    new_transaction['Amount'] = new_transaction['Amount'] + float(abs(insurance_amt))

            if 'BZ EVANS' in new_transaction['Description']:

                # Create a new transaction for the internet and append it to the expenses master file
                internet_amt = -70.50
                new_internet_transaction = {'Date': date, 'Description': 'Internet', 'Amount': internet_amt,
                                            'Transaction Type': 'debit', 'Category': 'Internet',
                                            'Account Name': account_name, 'Reference': reference}
                new_chase_transaction.append(new_internet_transaction)
                append_row_to_file(master_file, new_chase_transaction)
                new_chase_transaction = []

                # Deduct the internet amount from the rent transaction
                new_transaction['Amount'] = new_transaction['Amount'] + internet_amt

            # Append the transaction to the expenses master file
            new_chase_transaction.append(new_transaction)
            append_row_to_file(master_file, new_chase_transaction)
