import csv
import pandas as pd
hsbc_path = 'TransactionHistory.csv'
month = 11
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']


def upload_hsbc(csv_path):
    df = pd.read_csv(csv_path, names=['Date', 'Transaction', 'Amount'], parse_dates=[0], dayfirst=True)
    df2 = df[df['Date'].dt.strftime('%m') == str(month)]
    print(df2)


def main():
    upload_hsbc(hsbc_path)


if __name__ == "__main__":
    main()
