import gspread
import pandas as pd
from dataclasses import dataclass
from time import sleep
hsbc_path = 'TransactionHistory.csv'
month = 11
months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
# todo: Use the full miDataTransactions csv and a start and end date for the transactions and then automatically fill in the correct months
# todo: add other bank accounts. OOPify it. class for each account all inheriting from BankAccount parent class


@dataclass
class Transaction:
    date: str
    transaction_desc: str
    category: str
    amount: float


def get_hsbc_csv_data(csv_path):
    transactions = []
    # read in the csv and parse the date in date time format
    temp_df = pd.read_csv(csv_path, names=['date', 'transaction_desc', 'amount'], parse_dates=[0], dayfirst=True)
    # only get the month we are looking for
    df = temp_df[temp_df['date'].dt.strftime('%m') == str(month)]

    for _, row in df.iterrows():
        category = get_category(row[1])
        # use data class to create a formatted structure with all the information we need
        transactions.append(Transaction(str(row[0]).replace("00:00:00", ""), row[1], category, float(row[2].replace('\"', "").replace(",", ""))))
    return transactions


def get_category(transaction_desc):
    rent_and_bills_descs = ["VIRGIN MEDIA PYMTS DD", "BARCLAYS UK MTGES DD", "YORKSHIRE WATER DD", "OCTOPUS ENERGY DD"]
    if transaction_desc in rent_and_bills_descs:
        return "RENT & BILLS"
    elif transaction_desc == "CLUBWISE DD":
        return "Gym Membership"
    elif transaction_desc == "BOSCH THERMOTECH CR":
        return "Salary"
    return "other"


def upload_hsbc(csv_path):
    transactions = get_hsbc_csv_data(csv_path)
    # get service account details from %APPDATA%\gspread\service_account.json
    sevice_account = gspread.service_account()
    # open the correct sheet and worksheet and add the transactions
    sheet = sevice_account.open("Automated Personal Finances")
    worksheet = sheet.worksheet(months[month - 1])
    print("inserting rows...")
    for trans in transactions:
        worksheet.insert_row([trans.date, trans.transaction_desc, trans.category, trans.amount], 7)
        sleep(1)


def main():
    upload_hsbc(hsbc_path)


if __name__ == "__main__":
    main()
