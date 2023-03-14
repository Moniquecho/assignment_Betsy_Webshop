# Models go here
from peewee import *
import datetime

#Make a database
db = SqliteDatabase('BetsyWeb.db')

class BaseModel(Model):
    class Meta:
        database = db

#class about User information
class User(BaseModel):
    user_id = AutoField(unique = True)
    username =CharField(max_length=50)
    address = CharField()
    email = CharField()
    password = CharField()
    payment_info = CharField()

    class Meta:
        database = db

#class about product information 
class Product(BaseModel):
    product_id = AutoField (unique =True)
    name = CharField()
    description = TextField()
    price_per_unit =DecimalField(constraints = [Check('price_per_unit > 0')], decimal_places = 2, auto_round = False)
    quantity = IntegerField(default=1)
    user = ForeignKeyField(User)

    class Meta:
        database = db

class Tag(BaseModel):
    tag_id = AutoField(unique = True)
    name = CharField(null = False)

    class Meta:
        database = db

class Taggedproduct(BaseModel):
    Taggedproduct_id = AutoField (unique = True)
    product = ForeignKeyField(Product) 
    tag = ForeignKeyField(Tag)

    class Meta:
        database = db

class Transaction(BaseModel):
    Transaction_id = AutoField (unique = True)
    buyer = ForeignKeyField(User)
    purchase_product = ForeignKeyField(Product)
    purchased_quantity =IntegerField()
    purchased_date =DateField(formats='%d/%m/%Y', default=datetime.datetime.now)
    
    class Meta:
        database = db

