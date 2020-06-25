from src.read import TakeEmail
from src.transform import TransformData
from src.categories import Categories
import src.variables as var

e_mail = TakeEmail(var.username, var.pwd)
e_mail.connect_server()
emails = e_mail.fetch_data()
transform = TransformData(emails, var.username)
transform.verify_last_message_index()
df = transform.take_information()
categories = Categories(df)
categories.read_categories()
categories.verify_item_in_category()