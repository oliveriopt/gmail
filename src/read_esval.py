from src.read import TakeEmail


class ReadEsval():

    def __init__(self, username, pwd, email, path):
        self.username = username
        self.pwd = pwd
        self.email = email
        self.path = path

    def read_esval(self):
        e_mail = TakeEmail(self.username, self.pwd, self.path)
        e_mail.connect_server_extract_data(self.email)
        e_mail.flag_atachment = True
        e_mail.fetch_attachment()
