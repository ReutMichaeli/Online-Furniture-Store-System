from utils import get_index_of_product


class Order:
    payment_methods = ['Credit Card', 'PayPal', 'Cash on Delivery']
    order_id_counter = 1133

    def __init__(self, order_products, customer, products, payment_method=None):
        '''data initialization'''
        self.order_id = self._generate_order_id()
        self.order_products = order_products
        self.products = products
        self.customer = customer
        self.payment_method = payment_method
        self.payment_details = None
        self.total_price = self._calculate_total_price(products)
        self.status = "processing"

    def _generate_order_id(self):
        '''Gives order numbers'''
        Order.order_id_counter += 1
        return Order.order_id_counter

    def _calculate_total_price(self, products):
        '''The function calculates the total price of the order based on the quantity of products and their prices.'''
        total_price = 0
        for order_product in self.order_products:
            total_price += int(products[get_index_of_product(order_product["item_id"], products)].price) * int(
                order_product["quantity"])
        return total_price

    def update_status(self, order_id, new_status):
        '''update status'''
        self.status = new_status
        for order in self.orders:
            if order.order_id == order_id:
                order.update_status(new_status)
                break

    def choose_payment_method(self):
        '''Allows the user to select a payment method from a list of predefined payment methods, and updates the selected payment method in the variable'''
        while True:
            #print("Choose a payment method:")
            for index, method in enumerate(self.payment_methods, start=1):
                print(f"{index}. {method}")
            choice = input("Enter the number of your choice: ")
            if choice.isdigit() and 1 <= int(choice) <= len(self.payment_methods):
                self.payment_method = self.payment_methods[int(choice) - 1]
                break
            else:
                return False

    def update_amount(self, item_id, quantity):
        '''You find the index of the product in the list of products.
Calculates the prices according to the product
Reduces / increases the quantity in stock'''
        product_index = get_index_of_product(order_product["item_id"], self.products)
        product_price = self.products[product_index].price
        self.total_price += product_price * int(quantity)
        self.products[product_index].quantity -= int(quantity)
        self.order_products.append({"item_id": item_id, "quantity": quantity})

    def __str__(self):
        products_str = ''
        for order_product in self.order_products:
            curr_item_id = order_product["item_id"]
            curr_quantity = order_product["quantity"]
            products_str += f"Item id - {curr_item_id}, Quantity: {curr_quantity}" + '; '
        return f"Order ID: {self.order_id}, Products: < {products_str} >, Customer: {self.customer.__str__()}, Total Price: {self.total_price}, Status: {self.status}, Payment Method: {self.payment_method}"
