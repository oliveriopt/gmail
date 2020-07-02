from datetime import datetime

import src.variables as var
import pandas as pd
import re

pd.set_option('display.max_rows', 1000)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


class TransformData():

    def __init__(self, data_emails, username):
        self.outcome = pd.read_csv(var.path_outcome)
        self.email = data_emails
        self.index = None
        self.username = username
        pass

    def verify_last_message_index(self):
        if self.outcome.empty:
            self.last_date = datetime(2019, 6, 10)
        else:
            self.outcome.sort_values(by="date")
            self.last_date = self.outcome.at[0, "date"]
            self.last_date = datetime.strptime(self.last_date, '%Y-%m-%d %H:%M:%S')

    def take_information(self):
        df = pd.DataFrame(columns=self.outcome.columns.values)

        if self.username == "oliver.pozo.m@gmail.com":
            index = 0
            for item in self.email:
                date = re.search(r'\d{2}/\d{2}/\d{4}', item)
                hour = re.search(r'\d{2}:\d{2}', item)
                date = datetime.strptime(date.group() + " " + hour.group(), '%d/%m/%Y %H:%M')
                print(date)
                amount = item[item.index("$") + len("$"):item.index(" en")]
                amount = amount.replace(".", "")
                place = item[item.index(" en ") + len(" en "):item.index(" asociado ")]
                df.loc[index] = [self.username, date, int(amount), place.lower(), None]
                index += 1

        df = TransformData.delete_df_already_transformed(self, df)
        return df

    def delete_df_already_transformed(self, df):
        df.sort_values(by="date")
        df = df[df["date"] < self.last_date].reset_index(drop=True)
        return df
