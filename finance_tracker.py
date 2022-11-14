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
        print(f"inserting rows into {worksheet}...")
        worksheet.insert_rows(transactions, row=7)


class HSBCTransactions(BankTransactions):

    def get_csv_data(self):
        # read in the csv and parse the date in date time format
        temp_df = pd.read_csv(self.csv_path, names=['Date', 'Name', 'Amount'], parse_dates=[0], dayfirst=True)

        # only get the month we are looking for
        df = temp_df[temp_df['Date'].dt.strftime('%m') == str(self.month)]

        # Convert types and add relevant columns
        df.replace(',', '', regex=True, inplace=True)
        df = df.astype({'Date': 'str', 'Amount': 'float'})
        df.insert(3, "Bank", "HSBC", allow_duplicates=True)
        df.insert(2, "Category", "Other", allow_duplicates=True)
        df = self.get_category(df)

        # Ensure columns are in the right order
        df = df[['Date', 'Name', 'Category', 'Amount', 'Bank']]
        return df.values.tolist()

    def get_category(self, df):
        rent_and_bills_descs = ["VIRGIN MEDIA PYMTS DD", "BARCLAYS UK MTGES DD", "YORKSHIRE WATER DD", "OCTOPUS ENERGY DD"]
        for desc in rent_and_bills_descs:
            df.loc[df['Name'] == desc, 'Category'] = "Rent and Bills"

        df.loc[df['Name'] == "CLUBWISE DD", 'Category'] = "Gym Membership"
        df.loc[df['Name'] == "BOSCH THERMOTECH CR", 'Category'] = "Salary"
        return df


class MonzoTransactions(BankTransactions):
    def get_csv_data(self):
        # read in the csv and parse the date in date time format
        temp_df = pd.read_csv(self.csv_path, parse_dates=[1], dayfirst=True)
        # only get the month we are looking for
        df = temp_df[temp_df['Date'].dt.strftime('%m') == str(self.month)]
        df['Date'] = df['Date'].astype(str)
        df['Bank'] = "Monzo"
        df = df[['Date', 'Name', 'Category', 'Amount', 'Bank']]
        return df.values.tolist()


class AmexTransactions(BankTransactions):
    # ! To be implemented
    ...


def main():
    hsbc = HSBCTransactions(csv_path='TransactionHistory.csv', month=11)
    hsbc.upload()
    monzo = MonzoTransactions(csv_path='Monzo_November.csv', month=11)
    monzo.upload()


if __name__ == "__main__":
    main()
