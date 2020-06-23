from src.read import TakeEmail
import src.variables as var

e_mail = TakeEmail(var.username, var.pwd)
e_mail.connect_server()
e_mail.fetch_data()
print(e_mail.text_clean)