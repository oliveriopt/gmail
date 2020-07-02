from io import StringIO
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage
from pdfminer.layout import LAParams


class TransformPdf():

    def __init__(self, file: str):
        self.file = file
        self.rsrcmgr = PDFResourceManager()
        self.retstr = StringIO()
        self.codec = 'utf-8'
        self.laparams = LAParams()
        self.device = TextConverter(self.rsrcmgr, self.retstr, codec=self.codec, laparams=self.laparams)
        self.fp = open(self.file, 'rb')
        self.interpreter = PDFPageInterpreter(self.rsrcmgr, self.device)
        self.password = ""
        self.maxpages = 0
        self.caching = True
        self.pagenos = set()

    def convert_pdf_to_txt(self):
        for page in PDFPage.get_pages(self.fp, self.pagenos, maxpages=self.maxpages, password=self.password,
                                      caching=self.caching,
                                      check_extractable=True):
            self.interpreter.process_page(page)

        text = self.retstr.getvalue()

        self.fp.close()
        self.device.close()
        self.retstr.close()
        return text
