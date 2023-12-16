"""
1. Users should be able to search for products by their name or category.
2. Users should be able to add/remove/modify product items in their shopping cart.
3. Users can rate and add a review for a product.
"""

from enum import Enum

class AccountStatus(Enum):
    ACTIVE, CLOSED, BLACKLISTED, NONE = 1, 2, 3, 4

class Account:
    def __init__(self, username, password, email, phone, shipping_address, bank_account, status=AccountStatus.ACTIVE):
        self.username = username
        self.password = password
        self.email = email
        self.phone = phone
        self.shipping_address = shipping_address
        self.status = status
        self.bank_account = bank_account
    
class Customer:
    def __init__(self, cart, order):
        self.cart = cart
        self.order = order

    def get_shopping_cart(self):
        return self.cart
    
    def modify_item_to_cart(self, item, quantity):
        self.cart.add_item(item, quantity)
    
    def remove_item_to_cart(self, item):
        self.cart.remove_item(item)

class Guest(Customer):
    def __init__(self, cart, order):
        super().__init__(cart, order)

    def register_account(self):
        None

class Member(Customer):
    def __init__(self, cart, order, account):
        super().__init__(cart, order)
        self.account = account

class ProductCategory:
    def __init__(self, name, description):
        self.name = name
        self.description = description


class ProductReview:
    def __init__(self, rating, review, reviewer):
        self.rating = rating
        self.review = review
        self.reviewer = reviewer

class Product:
    def __init__(self, id, name, description, price, available_item_count, category, seller_account):
        self.product_id = id
        self.name = name
        self.description = description
        self.price = price
        self.category = category
        self.available_item_count = available_item_count
        self.seller = seller_account
        self.reviews = []
    
    def add_review(self, review):
        self.reviews.append(review)

    def get_available_count(self):
        return self.available_item_count
    
    def update_available_count(self, quantity):
        self.available_item_count += quantity
    
    def update_price(self, new_price):
        self.price = new_price

class Item:
    def __init__(self, product,  price):
        self.product = product
        self.quantity = 0
        self.price = price
    
    def update_quantity(self, quantity):
        self.quantity +=quantity
        self.product.update_available_count(-quantity)
    
    def remove(self):
        self.product.update_available_count(-self.quantity)

    def verify_item(self, quantity):
        return quantity<=self.product.get_available_count()

class ShoppingCart:
    def __init__(self):
        self.items = []
    
    def add_item(self, item, quantity):
        if item.verify_item(quantity) == False:
            print("The available items are less than the chosen quantity")
            return
        if item not in self.items:
            item.update_quantity(quantity)
            self.items.append(item)
        else:
            for ite in self.items:
                if ite.product == item.Product:
                    ite.update_quantity(quantity)
    
    def remove_item(self, item):
        if item in self.items:
            for ite in self.items:
                if ite.product == item.Product:
                    ite.remove()
                    self.items.remove(ite)

    def get_items(self):
        return self.items
    
    def checkout(self):
        None

class Catalog:
    def __init__(self):
        self.products = []

    def add_product(self, product):
        self.products.append(product)
    
    def search_products_by_name(self, name):
        return filter(lambda product: product.name == name, self.products)

    def search_products_by_category(self, category):
        return filter(lambda product: product.category == category, self.products)