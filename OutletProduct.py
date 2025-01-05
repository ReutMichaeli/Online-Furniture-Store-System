from Product import Product
from Factory import ImportProduct
from Factory import ProductFactory
from Factory import RegularProduct
from Factory import OutletProduct


class OutletProduct(Product):  # products out dated that on sale
    pass

    def __str__(self):
        if self.currency == 'CZK':
            price_czk = self.price * 23.70 - int(self.discount)  # כפילות העלות למטבע הצ'כי
            return f"Item ID: {self.item_id}, Name: {self.name}, Description: {self.description}, Price: {price_czk} CZK, Quantity: {self.quantity}, Discount: {self.discount}"
        elif self.currency == 'RON':
            price_ron = self.price * 4.67 - int(self.discount)
            return f"Item ID: {self.item_id}, Name: {self.name}, Description: {self.description}, Price: {price_ron} RON, Quantity: {self.quantity}, Discount: {self.discount}"
        else:
            return f"Item ID: {self.item_id}, Name: {self.name}, Description: {self.description}, Price: {str(int(self.price) - int(self.discount))} {self.currency}, Quantity: {self.quantity}, Discount: {self.discount}"
