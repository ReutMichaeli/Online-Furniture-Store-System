from Product import Product


class ProductFactory:
    '''A function that creates product types'''
    @staticmethod
    def create_product(product_type, item_id, name, description, price, quantity, currency='USD'):
        if product_type == 'regular':
            return RegularProduct(item_id, name, description, price, quantity, currency)
        elif product_type == 'import':
            return ImportProduct(item_id, name, description, price, quantity, currency)
        elif product_type == 'outlet':
            return OutletProduct(item_id, name, description, price, quantity, currency)
        else:
            raise ValueError("Invalid product type")


class RegularProduct(Product):
    '''A function that initializes objects of the RegularProduct class'''
    def __init__(self, item_id, name, description, price, quantity, currency, discount):
        super().__init__(item_id, name, description, price, quantity, currency)
        self.discount = discount

class ImportProduct(Product):
    '''A function that initializes objects of the ImportProduct class'''
    def __init__(self, item_id, name, description, price, quantity, currency, source, shipping_weeks):
        super().__init__(item_id, name, description, price, quantity, currency)
        self.source = source
        self.shipping_weeks = shipping_weeks

class OutletProduct(Product):
    pass