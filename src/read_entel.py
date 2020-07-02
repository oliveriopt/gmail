from src.read import TakeEmail


class ReadEntel():

    def __init__(self, username, pwd, email, path, init_year_month):
        self.username = username
        self.pwd = pwd
        self.email = email
        self.path = path
        self.body = []
        self.text_pdf = ""
        self.file = None
        self.init_year_month = init_year_month

    def read_entel(self):
        e_mail = TakeEmail(self.username, self.pwd, self.path)
        e_mail.connect_server_extract_data(self.email)
        e_mail.flag_atachment = True
        e_mail.fetch_attachment()
