from src.read import TakeEmail


class ReadGasValpo():

    def __init__(self, username, pwd, email, path):
        self.username = username
        self.pwd = pwd
        self.email = email
        self.path = path
        self.body = []

    def read_gas_valpo(self):
        e_mail = TakeEmail(self.username, self.pwd)
        e_mail.connect_server_extract_data(self.email)
        self.body = e_mail.fetch_body_bci(servicio="Gas Valpo")
