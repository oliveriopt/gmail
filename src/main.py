from src.read_banco_estado import ReadBancoEstado
from src.read_gas_valpo import ReadGasValpo
from src.read_entel import ReadEntel
from src.read_gastos_comunes import ReadGastosComunes
from src.read_esval import ReadEsval
from src.extract_info_pdf import ExtractInformationPDF
from src.transform import TransformData

import src.variables as var


e_mail_gastos_comunes = ReadGastosComunes(var.username_moni, var.pwd_moni, var.email_gastos_comunes,
                                          var.path_pdf_gastos_comunes)
e_mail_gastos_comunes.read_gastos_comunes()
#
e_mail_gastos_comunes = ReadGastosComunes(var.username_moni, var.pwd_moni, var.email_gastos_comunes_2,
                                          var.path_pdf_gastos_comunes)
e_mail_gastos_comunes.read_gastos_comunes()
#

extract_gastos_comunes = ExtractInformationPDF("gastos_comunes", var.path_pdf_gastos_comunes,
                                              var.path_outcome_gastos_comunes,
                                              var.init_year_month_gastos_comunes,
                                              var.end_year_month)
extract_gastos_comunes.run_transform_pdf()
e_mail_entel = ReadEntel(var.username_moni, var.pwd_moni, var.email_entel,
                                 var.path_pdf_entel)
e_mail_entel.read_entel()

extract_entel = ExtractInformationPDF("entel", var.path_pdf_entel, var.path_outcome_entel, var.init_year_month_entel,
                                      var.end_year_month)
extract_entel.run_transform_pdf()
#
pdf_esval = ReadEsval(var.username_moni, var.pwd_moni, var.email_esval, var.path_pdf_esval)
pdf_esval.read_esval()

extract_esval = ExtractInformationPDF("esval", var.path_pdf_esval, var.path_outcome_esval, var.init_year_month_esval,
                                      var.end_year_month)
extract_esval.run_transform_pdf()
#
e_mail_gas_valpo = ReadGasValpo(var.username_moni, var.pwd_moni, var.email_gas_valpo, None, var.path_outcome_gas_valpo)
e_mail_gas_valpo.read_gas_valpo()
e_mail_gas_valpo.transform_bci()

extract_gas_valpo = ExtractInformationPDF("gas_valpo", var.path_pdf_gas_valpo,
                                          var.path_outcome_gas_valpo,
                                          var.init_year_month_gas_valpo,
                                          var.end_year_month)
extract_gas_valpo.run_transform_pdf()

e_mail_banco_estado = ReadBancoEstado(var.username_oli, var.pwd_oli, var.email_banco_estado, None)
e_mail_banco_estado.read_banco_estado()

transform = TransformData(e_mail_banco_estado.body, var.username_oli)
transform.verify_last_message_index()
df = transform.take_information()
categories = Categories(df)
categories.read_categories()
categories.verify_item_in_category()


#




