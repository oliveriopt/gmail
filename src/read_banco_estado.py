from src.read import TakeEmail


class ReadBancoEstado():

    def __init__(self, username, pwd, email):
        self.username = username
        self.pwd = pwd
        self.email = email
        self.body = []

    def read_banco_estado(self):
        e_mail = TakeEmail(self.username, self.pwd)
        e_mail.connect_server_extract_data(self.email)
        self.body = e_mail.fetch_data(self.email)
