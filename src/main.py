from src.read_banco_estado import ReadBancoEstado
from src.read_gas_valpo import ReadGasValpo
from src.read_entel import ReadEntel
from src.read_gastos_comunes import ReadGastosComunes
from src.read_esval import ReadEsval

import src.variables as var

#e_mail_banco_estado = ReadBancoEstado(var.username_oli, var.pwd_oli, var.email_banco_estado, None)
#e_mail_banco_estado.read_banco_estado()
# print(e_mail_banco_estado.body)
#
e_mail_gastos_comunes = ReadGastosComunes(var.username_moni, var.pwd_moni, var.email_gastos_comunes,
                                           var.path_pdf_gastos_comunes)
e_mail_gastos_comunes.read_gastos_comunes()

pdf_esval = ReadEsval(var.username_moni, var.pwd_moni, var.email_esval, var.path_pdf_esval)
pdf_esval.read_esval()

#e_mail_gas_valpo = ReadGasValpo(var.username_moni, var.pwd_moni, var.email_gas_valpo, None)
#e_mail_gas_valpo.read_gas_valpo()
#print(len(e_mail_gas_valpo.body))

e_mail_entel = ReadEntel(var.username_moni, var.pwd_moni, var.email_entel,
                                 var.path_pdf_entel)
e_mail_entel.read_entel()

# transform = TransformData(emails, var.username_oli)
# transform.verify_last_message_index()
# df = transform.take_information()
# categories = Categories(df)
# categories.read_categories()
# categories.verify_item_in_category()
