import gspread
import pandas as pd

# todo: Use the full miDataTransactions csv and a start and end date for the transactions and then automatically fill in the correct months


class BankTransactions():
    def __init__(self, csv_path, month):
        self.csv_path = csv_path
        self.month = month

    def get_csv_data(self):
        pass

    def get_category(self):
        pass

    def upload(self):
        months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
        transactions = self.get_csv_data()
        # get service account details from %APPDATA%\gspread\service_account.json
        sevice_account = gspread.service_account()
        # open the correct sheet and worksheet and add the transactions
        sheet = sevice_account.open("Automated Personal Finances")
        worksheet = sheet.worksheet(months[self.month - 1])
        print(f"inserting rows into {months[self.month - 1]}...")
        worksheet.insert_rows(transactions, row=7)


class HSBCTransactions(BankTransactions):
    def get_transaction_history(self):
        # read in the csv and parse the date in date time format
        temp_df = pd.read_csv(self.csv_path, names=['Date', 'Name', 'Amount'], parse_dates=[0], dayfirst=True)
        # only get the month we are looking for
        df = temp_df[temp_df['Date'].dt.strftime('%m') == str(self.month).zfill(2)]
        # Convert types and add relevant columns
        df = df.replace(',', '', regex=True)
        df = df.astype({'Date': 'str', 'Amount': 'float'})
        df.insert(3, "Bank", "HSBC", allow_duplicates=True)
        df.insert(2, "Category", "Other", allow_duplicates=True)
        df = self.get_category(df, 'Name')

        # Ensure columns are in the right order
        df = df[['Date', 'Name', 'Category', 'Amount', 'Bank']]
        return df.values.tolist()

    def get_midata_transactions(self):
        # read in the csv and parse the date in date time format
        temp_df = pd.read_csv(self.csv_path, parse_dates=[0], dayfirst=True)
        # only get the month we are looking for
        df = temp_df[temp_df['Date'].dt.strftime('%m') == str(self.month).zfill(2)]
        # # Convert types and add relevant columns
        df = df.replace(',', '', regex=True)
        df = df.replace('£', '', regex=True)

        df = df.astype({'Date': 'str', 'Debit/Credit': 'float'})
        df.insert(3, "Bank", "HSBC", allow_duplicates=True)
        df.insert(2, "Category", "Other", allow_duplicates=True)
        df = self.get_category(df, 'Merchant/Description')

        # # Ensure columns are in the right order
        df = df[['Date', 'Merchant/Description', 'Category', 'Debit/Credit', 'Bank']]
        return df.values.tolist()

    def get_csv_data(self):
        # transactions = self.get_midata_transactions()
        transactions = self.get_transaction_history()

        return transactions

    def get_category(self, df, desc_header):
        rent_and_bills_descs = ["VIRGIN MEDIA PYMTS DD", "BARCLAYS UK MTGES DD", "YORKSHIRE WATER DD", "OCTOPUS ENERGY DD"]
        for desc in rent_and_bills_descs:
            df.loc[df[desc_header] == desc, 'Category'] = "Rent and Bills"

        df.loc[df[desc_header] == "CLUBWISE DD", 'Category'] = "Gym Membership"
        df.loc[df[desc_header] == "BOSCH THERMOTECH CR", 'Category'] = "Salary"
        df.loc[df[desc_header] == "VANGUARD ASSET MAN", 'Category'] = "Investments"

        return df


class MonzoTransactions(BankTransactions):
    def get_csv_data(self):
        # read in the csv and parse the date in date time format
        temp_df = pd.read_csv(self.csv_path, parse_dates=[1], dayfirst=True)
        # only get the month we are looking for
        df = temp_df[temp_df['Date'].dt.strftime('%m') == str(self.month).zfill(2)]
        df = df.astype({'Date': 'str', 'Amount': 'float'})
        df.insert(3, "Bank", "Monzo", allow_duplicates=True)
        df = df[['Date', 'Name', 'Category', 'Amount', 'Bank']]
        return df.values.tolist()


class AmexTransactions(BankTransactions):
    # ! To be implemented
    ...


def main():
    month = 11
    hsbc = HSBCTransactions(csv_path='TransactionHistory.csv', month=month)
    hsbc.upload()
    monzo = MonzoTransactions(csv_path='MonzoDataExport_1Jan-14Nov_2022-11-14_161142.csv', month=month)
    monzo.upload()


if __name__ == "__main__":
    main()
