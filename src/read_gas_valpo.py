from src.read import TakeEmail

import re
import pandas as pd
from datetime import datetime

pd.set_option('display.max_rows', 1000)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


class ReadGasValpo():

    def __init__(self, username, pwd, email, path, path_outcome):
        self.username = username
        self.pwd = pwd
        self.email = email
        self.path = path
        self.path_outcome = path_outcome
        self.body = []

    def read_gas_valpo(self) -> None:
        """
        Fetcch the body for Gas VAlpo
        """
        e_mail = TakeEmail(self.username, self.pwd, self.path)
        e_mail.connect_server_extract_data(self.email)
        self.body = e_mail.fetch_body_bci(servicio="Gas Valpo")
        self.body = list(set(self.body))

    def transform_bci(self):
        pd_gas_valpo = pd.DataFrame(columns=["Date", "Amount"])
        index = 0
        for item in self.body:
            date = item[item.find('fecha') + 6:item.find('se') - 1]
            amount = item[item.find('$'):item.find('$') + 8]
            result = re.split('\s+', amount)
            amount = result[0]
            amount = re.sub('[^0-9,.]', ' ', amount)
            amount = amount.replace(".", "").replace(",", ".").rstrip()
            pd_gas_valpo.loc[index] = [datetime.strptime(date, '%d/%m/%Y'), amount]
            index += 1
        pd_gas_valpo = pd_gas_valpo.drop_duplicates(keep='first').sort_values(by="Date").reset_index(
            drop=True)
        pd_gas_valpo.to_csv(self.path_outcome, index=False)
