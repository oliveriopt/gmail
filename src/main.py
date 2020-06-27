from src.read_banco_estado import ReadBancoEstado
from src.read_gastos_comunes import ReadGastosComunes
from src.read_esval import ReadEsval

import src.variables as var

# e_mail_banco_estado = ReadBancoEstado(var.username_oli, var.pwd_oli, var.email_banco_estado, None)
# e_mail_banco_estado.read_banco_estado()
# print(e_mail_banco_estado.body)
#
# e_mail_gastos_comunes = ReadGastosComunes(var.username_moni, var.pwd_moni, var.email_gastos_comunes,
#                                           var.path_gastos_comunes)
# e_mail_gastos_comunes.read_gastos_comunes()

pdf_esval = ReadEsval(var.username_moni, var.pwd_moni, var.email_esval, var.path_esval)
pdf_esval.read_esval()

# transform = TransformData(emails, var.username_oli)
# transform.verify_last_message_index()
# df = transform.take_information()
# categories = Categories(df)
# categories.read_categories()
# categories.verify_item_in_category()
