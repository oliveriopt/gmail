from bs4 import BeautifulSoup
from datetime import datetime

import src.variables as var
import imaplib
import email
import re
import os
import pikepdf


class TakeEmail:

    def __init__(self, username: str, pwd: str, path_pdf: str):
        self.imap_ssl_host = var.SMTP_SERVER
        self.imap_ssl_port = var.SMTP_PORT
        self.username = username
        self.password = pwd
        self.server = imaplib.IMAP4_SSL(self.imap_ssl_host, self.imap_ssl_port)
        self.text_clean = []
        self.flag_atachment = False
        self.path_pdf = path_pdf

    def connect_server_extract_data(self, email_extract) -> None:
        """"
        Connect server and fectch data
        """
        self.server.login(self.username, self.password)
        self.server.select()
        string_extract = '(OR (TO "' + email_extract + '") (FROM "' + email_extract + '"))'
        self.status, self.data = self.server.search(None, string_extract)
        if self.flag_atachment:
            self.status, self.data = self.server.search(None, 'FROM', "'" + email_extract + "'")

    def fetch_body_banco_estado(self) -> str:
        """
        Fetch body of email
        :return:
        """

        self.text_clean = []
        for num in self.data[0].split():
            status, data = self.server.fetch(num, '(RFC822)')
            raw_email = data[0][1]
            msg = email.message_from_bytes(raw_email)
            for part in msg.walk():
                text = part.get_payload()
                soup = BeautifulSoup(text, 'lxml')
                clean_text = soup.get_text()
                clean_text = re.sub('=', ' ', clean_text)
                clean_text = clean_text.replace("\r\n", " ")
                clean_text = re.sub(' +', ' ', clean_text)
                self.text_clean.append(clean_text)
        return self.text_clean

    def fetch_body_bci(self, servicio: str) -> None:
        """
        Fetch body of email from BCI
        :param servicio: kind of service
        :return:
        """

        self.text_clean = []
        for num in self.data[0].split()[:]:
            status, data = self.server.fetch(num, '(RFC822)')
            raw_email = data[0][1]
            msg = email.message_from_bytes(raw_email)
            for part in msg.walk():
                text = part.get_payload()
                if isinstance(text, str):
                    clean_text = BeautifulSoup(text, "lxml")
                    clean_text = clean_text.get_text()
                    if clean_text.find(servicio) != -1:
                        clean_text = re.sub('=', '', clean_text)
                        clean_text = clean_text.replace("\r\n", " ")
                        clean_text = clean_text.replace("\n", " ")
                        clean_text = clean_text.replace("\t", " ")
                        clean_text = re.sub(' +', ' ', clean_text)
                        self.text_clean.append(clean_text)
                temp = []
                if isinstance(text, list):
                    for item in text:
                        txt = item.get_payload()
                        clean_text = BeautifulSoup(txt, "lxml")
                        clean_text = clean_text.get_text()
                        if clean_text.find(servicio) != -1:
                            clean_text = re.sub('=', '', clean_text)
                            clean_text = clean_text.replace("\r\n", " ")
                            clean_text = clean_text.replace("\n", " ")
                            clean_text = clean_text.replace("\t", " ")
                            clean_text = re.sub(' +', ' ', clean_text)
                            temp = temp + [clean_text]
                if len(temp) > 0:
                    self.text_clean.extend(temp)
        return self.text_clean

    def fetch_attachment_esval(self, filename: str, date: datetime) -> None:
        """
        Fetch attachment from esval
        :param filename: name of the file
        :param date: date to process
        :return:
        """
        os.rename(self.path_pdf + filename,
                  self.path_pdf + date.strftime("%Y") + "_" + date.strftime("%m") + ".pdf")
        if filename.endswith(".xml"):
            os.remove(self.path_pdf + date.strftime("%Y") + "_" + date.strftime("%m") + ".pdf")

    def fetch_attachment_entel(self, filename: str, date: datetime) -> None:
        """
        Fetch attachment of entel
        :param filename:
        :param date:
        :return:
        """
        os.rename(self.path_pdf + filename,
                  self.path_pdf + date.strftime("%m") + "_" + date.strftime("%Y") + "_" + \
                  filename)
        try:
            init_pdf = pikepdf.open(
                self.path_pdf + date.strftime("%m") + "_" + date.strftime("%Y") + "_"
                + \
                filename, password='4713')
            new_pdf = pikepdf.new()
            new_pdf.pages.extend(init_pdf.pages)
            new_pdf.save(str(self.path_pdf + date.strftime("%Y") + "_" + date.strftime("%m") + ".pdf"))
            os.remove(self.path_pdf + date.strftime("%m") + "_" + date.strftime("%Y") + "_" + \
                      filename)
        except:
            os.remove(self.path_pdf + date.strftime("%m") + "_" + date.strftime("%Y") + "_" + \
                      filename)
            pass

    def fetch_attachment_gastos_comunes(self, filename, date):
        if "Gastos comunes departamento 1102" in filename:
            os.rename(self.path_pdf + filename,
                  self.path_pdf + date.strftime("%Y") + "_" + date.strftime("%m") + ".pdf")

        else:
            os.remove(self.path_pdf + filename)
        pass

    def fetch_attachment(self) -> None:
        """
        Fetch attachement from email
        :return:
        """

        items = self.data[0].split()
        for item in items:
            status, data = self.server.fetch(item, '(RFC822)')
            raw = email.message_from_bytes(data[0][1])
            print(raw["Date"])
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

                att_path = os.path.join(self.path_pdf, filename)
                # Check if its already there

                if not os.path.isfile(att_path):
                    # finally write the stuff
                    fp = open(att_path, 'wb')
                    fp.write(part.get_payload(decode=True))
                    fp.close()

                    if "esval" in self.path_pdf:
                        TakeEmail.fetch_attachment_esval(self, filename, date)

                    if "entel" in self.path_pdf:
                        TakeEmail.fetch_attachment_entel(self, filename, date)

                    if "gastos_comunes" in self.path_pdf:
                        TakeEmail.fetch_attachment_gastos_comunes(self, filename, date)
