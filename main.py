from datetime import datetime  # core python module
import pandas as pd  # pip install pandas
from send_email import send_email  # local python module

URL = 'invoice_data - Sheet1.csv'

def load_df(url):
    parse_dates = ["due_date", ]
    df = pd.read_csv(url, parse_dates=parse_dates)
    return df
    

def query_data_and_send_emails(df):
    email_counter = 0
    for _, row in df.iterrows():
        send_email(
                subject = f'[Invoice Reminder] Invoice: {row["invoice_no"]}',
                email_receiver=row["email"],
                name = row["name"],
                invoice_no=row["invoice_no"],
                amount=row["amount"],
                due_date=row["due_date"].strftime("%d, %b %Y") # example: 11, Aug 2022
            )
        email_counter += 1
    return f"Total Emails Sent: {email_counter}"



df = load_df(URL)
result = query_data_and_send_emails(df)
print(result)
