__winc_id__ = "d7b474e9b3a54d23bca54879a4f1855b"
__human_name__ = "Betsy Webshop"

from models import *
import os
from spellchecker import SpellChecker

spell = SpellChecker()

def search(term):
    term = term.lower()
    misspelled_word = spell.correction(term)
    product_name = Product.name.contains(term)
    misspelled_product_name = Product.name.contains(misspelled_word)
    product_description = Product.description.contains(term)
    misspelled_product_description = Product.description.contains(misspelled_word)
    
    query = Product.select().where(product_name | product_description |misspelled_product_name| misspelled_product_description)
    if query.exists():
        for product in query:
            print(f"It is found with your search {term}!")
            print(product.name)
    else:
        print(f"It is not found with your search term {term}.")

def list_user_products(user_id):
    query = Product.select().where(Product.user == user_id).order_by(Product.name)
    
    if query:
        print(list(product.name for product in query))
    else:
        print(f"There is no product with user_id.")

    
def list_products_per_tag(tag_id):
    query = Product.select().join(Taggedproduct).join(Tag).where(Tag.tag_id == tag_id).order_by(Product.name)
    
    if query:
        print(f"Here are tegged_products.")
        print(list(product.name for product in query))
    else:
        print(f"There is no tagged product with {tag_id}")


def add_product_to_catalog(user_id, product_name, description, price, quantity ):
    new_product = Product.insert(name = product_name, description= description, price_per_unit = price, quantity =quantity, user=user_id )
    new_product.execute()
    print(f"New product {product_name} from user_id:{user_id} is added ")
    return new_product 

def update_stock(product_id, new_quantity):
    product = Product.get_by_id(product_id)
    product.quantity == new_quantity
    product.save()
    print (f"There are now {product.name} , {new_quantity} times in stock.")

    
def purchase_product(product_id, buyer_id, quantity):
    product = Product.get_by_id(product_id)
    
    if quantity > product.quantity:
        print(f"Sorry! Not enough product{product.name} in stock")
    
    else:
        new_quantity = product.quantity - quantity
        update_stock(product_id, new_quantity)

        transaction = Transaction.create(
            buyer=buyer_id, 
            purchase_product=product_id, 
            purchased_quantity = quantity, 
            purcased_date=datetime.now().date())
        print(f"product{product.name} with {transaction.purchased_quantity} was sold on the date {transaction.purchased_date}.")
        

def remove_product(product_id):
    product = Product.delete().where(Product.product_id == product_id)
    product.execute()
    print(f"Product id:{product_id} removed from catalog.")

# Make a test database
def populate_test_database():
    db.connect()
# Create a folder in a current location.
    cwd = os.getcwd()
    print(f"A folder about database of BetsyWeb is created.")

# Create tables of all the classes from model.py
    db.create_tables([User, Tag, Taggedproduct, Product, Transaction])

    Boaz = User.create(username = "Boaz", address = "symponielaan 23", email = "bo@gmail.com", password = 123,payment_info = 123)
    Bradley = User.create(username = "Bradley", address = "bethoveenlaan 11", email ="br@gmail.com",password = 123,payment_info = 234)
    Emma = User.create(username = "Emma", address = "mozartweg 7", email = "em@gmail.com",password =123, payment_info = 136)
    Janita = User.create(username = "Janita", address = "listlaan 25", email ="ja@gmail.com", password =234, payment_info = 1789)
    Lieke = User.create(username = "Lieke", address = "chopinweg 21", email ="li@gmail.com", password =456, payment_info = 199)
  
    overalljeans = Product.create(name = "overalljeans", description = "comfortable jeans", price_per_unit = 5, quantity = 2, user =Boaz)
    couch = Product.create(name = "couch", description = "used sofa, nice to read a book", price_per_unit = 10, quantity = 3, user = Bradley)
    raincoat = Product.create(name = "raincoat", description = "warm coat and nice black color", price_per_unit = 9, quantity =1, user =Boaz)
    ring = Product.create(name = "ring", description = "small size but design is athentic", price_per_unit = 6, quantity = 5, user = Bradley)
    umbrella = Product.create(name = "umbrella", description = "big enough for two people in the rain", price_per_unit = 3, quantity = 6, user = Emma)

    jeans = Tag.create(name="jeans")
    rain = Tag.create(name= "rain")
    cloth = Tag.create(name= "cloth")
    accessory = Tag.create(name= "accessory")
    funiture = Tag.create(name= "funiture")
    
    Taggedproduct.create(product = overalljeans, tag = jeans)
    Taggedproduct.create(product = raincoat, tag = rain)
    Taggedproduct.create(product = couch, tag = funiture)
    Taggedproduct.create(product = ring, tag = accessory)
    Taggedproduct.create(product = umbrella, tag = rain)
 
    

def main():
                                             
    populate_test_database()
    print("")
    search("rain") # search a product name or description with a valid term 
    print("")  
    search("shoes") # search a product with an invalid term
    print("")  
    search("raincoa") # search a product with a misspelled term
    print("")  
    list_user_products(1) # list user products
    print("")  
    list_products_per_tag(2) # list products per tag
    print("")  
    list_products_per_tag(100) # list products per invalid tag
    print("") 
    add_product_to_catalog(1, "shoes","comfortable", 2, 5)# add product to catalog
    print("")  
    update_stock(2, 5) # update stock with a new product
    print("")  
    purchase_product(3, 1, 2) # purchase a product by user
    print("")  
    remove_product(5) # remove a product from a stock
    print("")  

if __name__ == '__main__':
    main()
