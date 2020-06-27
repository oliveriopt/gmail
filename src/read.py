from bs4 import BeautifulSoup
from datetime import datetime

import src.variables as var
import imaplib
import email
import re
import os


class TakeEmail():

    def __init__(self, username, pwd):
        self.imap_ssl_host = var.SMTP_SERVER
        self.imap_ssl_port = var.SMTP_PORT
        self.username = username
        self.password = pwd
        self.server = imaplib.IMAP4_SSL(self.imap_ssl_host, self.imap_ssl_port)
        self.text_clean = []
        self.flag_atachment = False

    def connect_server_extract_data(self, email_extract):
        """"
        Connect server and fectch data
        """
        self.server.login(self.username, self.password)
        self.server.select()
        string_extract = '(OR (TO "' + email_extract + '") (FROM "' + email_extract + '"))'
        self.status, self.data = self.server.search(None, string_extract)
        if self.flag_atachment:
            self.status, self.data = self.server.search(None, 'FROM', "'" + email_extract + "'")

    def fetch_body(self) -> None:

        self.text_clean = []
        for num in self.data[0].split():
            status, data = self.server.fetch(num, '(RFC822)')
            raw_email = data[0][1]
            msg = email.message_from_bytes(raw_email)
            for part in msg.walk():
                text = part.get_payload()
                clean_text = BeautifulSoup(text, "lxml").text
                clean_text = re.sub('=', '', clean_text)
                clean_text = clean_text.replace("\r\n", "")
                clean_text = re.sub(' +', ' ', clean_text)
                self.text_clean.append(clean_text)
        return self.text_clean

    def fetch_attachment(self, path_pdf: str) -> None:

        items = self.data[0].split()
        for item in items:
            status, data = self.server.fetch(item, '(RFC822)')
            raw = email.message_from_bytes(data[0][1])
            print(raw['Date'])
            if "GMT" in raw['Date']:
                date = datetime.strptime(raw['Date'][:-12], "%a, %d %b %Y %H:%M:%S %z")
            else:
                date = datetime.strptime(raw['Date'], "%a, %d %b %Y %H:%M:%S %z")
            for part in raw.walk():
                if part.get_content_maintype() == 'multipart':
                    pass

                # is this part an attachment ?
                if part.get('Content-Disposition') is None:
                    pass

                filename = part.get_filename()
                counter = 1

                # if there is no filename, we create one with a counter to avoid duplicates
                if not filename:
                    filename = 'part-%03d%s' % (counter, 'bin')
                    counter += 1

                att_path = os.path.join(path_pdf, filename)
                # Check if its already there

                if not os.path.isfile(att_path):
                    # finally write the stuff
                    fp = open(att_path, 'wb')
                    fp.write(part.get_payload(decode=True))
                    fp.close()
                    os.rename(path_pdf + filename, path_pdf + date.strftime("%b") + "_" + date.strftime("%Y") + "_" + \
                              filename)
