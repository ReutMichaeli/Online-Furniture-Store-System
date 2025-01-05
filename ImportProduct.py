from Product import Product
from Factory import ImportProduct
from Factory import ProductFactory
from Factory import RegularProduct
from Factory import OutletProduct

class ImportProduct(Product):  # products from oversea
    def __init__(self):
        pass

    def __str__(self):
        if self.currency == 'CZK':
            price_czk = self.price * 23.70  # כפילות העלות למטבע הצ'כי
            return f"Item ID: {self.item_id}, Name: {self.name}, Description: {self.description}, Price: {price_czk} CZK, Quantity: {self.quantity}, Source country: {self.source}, Shipping weeks time: {self.shipping_weeks}"
        elif self.currency == 'RON':
            price_ron = self.price * 4.67
            return f"Item ID: {self.item_id}, Name: {self.name}, Description: {self.description}, Price: {price_ron} RON, Quantity: {self.quantity}, Source country: {self.source}, Shipping weeks time: {self.shipping_weeks}"
        else:
            return f"Item ID: {self.item_id}, Name: {self.name}, Description: {self.description}, Price: {self.price} {self.currency}, Quantity: {self.quantity}, Source country: {self.source}, Shipping weeks time: {self.shipping_weeks}"
