from src.read import TakeEmail


class ReadBCI:

    def __init__(self, username, pwd, email, path):
        self.username = username
        self.pwd = pwd
        self.email = email
        self.path = path
        self.body = []

    def read_bci(self)->None:
        """
        Fetch body of BCI
        :return:
        """
        e_mail = TakeEmail(self.username, self.pwd, None)
        e_mail.connect_server_extract_data(self.email)
        self.body = e_mail.fetch_body_bci_debito()