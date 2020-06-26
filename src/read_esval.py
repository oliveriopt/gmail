from src.read import TakeEmail


class ReadEsval():

    def __init__(self, username, pwd, email):
        self.username = username
        self.pwd = pwd
        self.email = email

    def read_esval(self):
        e_mail = TakeEmail(self.username, self.pwd)
        e_mail.connect_server_extract_data(self.email)
        e_mail.fetch_attachment(self.email)
