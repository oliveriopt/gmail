from bs4 import BeautifulSoup

import src.variables as var
import imaplib
import email
import re


class TakeEmail():

    def __init__(self, username, pwd):
        self.imap_ssl_host = var.SMTP_SERVER
        self.imap_ssl_port = var.SMTP_PORT
        self.username = username
        self.password = pwd
        self.server = imaplib.IMAP4_SSL(self.imap_ssl_host, self.imap_ssl_port)
        self.text_clean = []

    def connect_server(self):
        """"
        Connect server and fectch data
        """
        self.server.login(self.username, self.password)
        self.server.select()
        self.status, self.data = self.server.search(None,
                                                    '(OR (TO "notificaciones@bancoestado.cl") (FROM "notificaciones@bancoestado.cl"))')

    def fetch_data(self):
        """"
        Fetch data
        """

        for num in self.data[0].split():
            status, data = self.server.fetch(num, '(RFC822)')
            raw_email = data[0][1]
            msg = email.message_from_bytes(raw_email)
            for part in msg.walk():
                text = part.get_payload()
                cleantext = BeautifulSoup(text, "lxml").text
                cleantext = re.sub('=', '', cleantext)
                cleantext = cleantext.replace("\r\n", "")
                cleantext = re.sub(' +', ' ', cleantext)
                self.text_clean.append(cleantext)
        return self.text_clean
