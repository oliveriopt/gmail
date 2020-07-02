from src.transform_pdf import TransformPdf
from dateutil.relativedelta import relativedelta
from datetime import datetime, date, timedelta

import src.variables as var
import os


class ExtractInformationPDF():

    def __init__(self, service, path, path_outcome, inti_year_month, end_year_month):
        self.service = service
        self.path = path
        self.path_outcome = path_outcome
        self.init_year_month = inti_year_month
        self.end_year_month = end_year_month
        self.file = None
        self.text_pdf = None

    def transform_pdf(self):
        transform_pdf = TransformPdf(self.path + self.file)
        self.text_pdf = transform_pdf.convert_pdf_to_txt()

    def next_month(self, next):
        if not next.month % 12:
            next = date(next.year + 1, 1, 1)
        else:
            next = date(next.year, next.month + 1, 1)
        return next

    def name_file(self, next):
        if int(next.month) < 10:
            self.file = str(next.year) + "_0" + str(next.month) + ".pdf"
        else:
            self.file = str(next.year) + "_" + str(next.month) + ".pdf"

    def filter_text(self):
        self.text_pdf = self.text_pdf.replace("\n", " ")

    def extract_entel_esval(self):

        x = self.text_pdf[self.text_pdf.find('$') + 2:]
        amount = int(x[:x.find(" ")].replace(".", ""))
        return amount

    def write_file(self, date, amount):
        if amount is None:
            if os.path.isfile(self.path_outcome):
                os.remove(self.path_outcome)
            file = open(self.path_outcome, 'a')
            file.write("Date,Amount\n")
        else:
            file = open(self.path_outcome, 'a')
            file.write("%s,%d\n" % (date, amount))
        file.close()


    def run_transform_pdf(self):
        """

        :return:
        """
        r = relativedelta(self.end_year_month, self.init_year_month)
        next = self.init_year_month
        ExtractInformationPDF.write_file(self, "xx", None)
        for month in range((r.years * 12) + r.months):
            ExtractInformationPDF.name_file(self, next)
            if os.path.isfile(self.path + self.file):
                ExtractInformationPDF.transform_pdf(self)
                ExtractInformationPDF.filter_text(self)
                if self.service == "entel":
                    ExtractInformationPDF.write_file(self, next, ExtractInformationPDF.extract_entel_esval(self))
                if self.service == "esval":
                    ExtractInformationPDF.write_file(self, next, ExtractInformationPDF.extract_entel_esval(self))

            next = ExtractInformationPDF.next_month(self, next)


extract_entel = ExtractInformationPDF("entel", var.path_entel, var.path_outcome_entel, var.init_year_month_entel,
                                      var.end_year_month)
extract_entel.run_transform_pdf()

extract_esval = ExtractInformationPDF("esval", var.path_esval, var.path_outcome_esval, var.init_year_month_esval,
                                      var.end_year_month)
print("ok")
extract_esval.run_transform_pdf()
