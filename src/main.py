from src.read import TakeEmail
from src.transform import TransformData
from src.categories import Categories
import src.variables as var

e_mail = TakeEmail(var.username_oli, var.pwd_oli)
e_mail.connect_server_extract_data(var.email_banco_estado)
emails = e_mail.fetch_data(var.email_banco_estado)

print(emails)

e_mail = TakeEmail(var.username_moni, var.pwd_moni)
e_mail.connect_server_extract_data(var.email_esval)
e_mail.fetch_data(var.email_esval)

#transform = TransformData(emails, var.username_oli)
#transform.verify_last_message_index()
#df = transform.take_information()
#categories = Categories(df)
#categories.read_categories()
#categories.verify_item_in_category()