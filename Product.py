class Product:
    def __init__(self, item_id, name, description, price, quantity, currency='USD'):
        '''data initialization'''
        self.item_id = item_id
        self.name = name
        self.description = description
        self.price = int(price)
        self.quantity = int(quantity)
        self.currency = currency
        self.reviews = []

    def add_review(self, customer_id, review, rating):
        '''Checks that the rating is a number'''
        if rating.isdigit() and 1 <= int(rating) <= 5:
            self.reviews.append({'customer_id': customer_id, 'review': review, 'rating': int(rating)})
            return True
        else:
            return False

    def __contains__(self):
        '''How an instance of a class will be treated when the in operator is used on it.'''
        if self.reviews:
            print(f"Reviews for {self.name}:")
            for review in self.reviews:
                print(f"Customer ID: {review['customer_id']}, Review: {review['review']}, Rating: {review['rating']}")
        else:
            None

    def __add__(self, name, description, price, quantity):
        '''A function that initializes data in order to add'''
        self.name = name
        self.description = description
        self.price = int(price)
        self.quantity = int(quantity)

    def __str__(self):
        if self.currency == 'CZK':
            price_czk = self.price * 23.70  # כפילות העלות למטבע הצ'כי
            return f"Item ID: {self.item_id}, Name: {self.name}, Description: {self.description}, Price: {price_czk} CZK, Quantity: {self.quantity}"
        elif self.currency == 'RON':
            price_ron = self.price * 4.67
            return f"Item ID: {self.item_id}, Name: {self.name}, Description: {self.description}, Price: {price_ron} RON, Quantity: {self.quantity}"
        else:
            return f"Item ID: {self.item_id}, Name: {self.name}, Description: {self.description}, Price: {self.price} {self.currency}, Quantity: {self.quantity}"


