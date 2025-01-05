import datetime
import os
import random
import re
import json
from urllib.request import urlopen, Request
from urllib.parse import urlencode
import csv
from abc import ABC, abstractmethod
from LanguageTranslator import LanguageTranslator
from Customer import Customer
from Product import Product
from Review import Review
from Product import Product
from order import Order
from PaymentProcessor import PaymentProcessor
from DataLayer import DataLayer
from ImportProduct import ImportProduct
from OutletProduct import OutletProduct
from utils import choose_language, print_welcome_message, login, check_if_customer_id_exists, check_if_order_id_exists, check_if_product_id_exists, get_customer, get_index_of_product
from Singleton import Singleton
from Factory import ImportProduct
from Factory import ProductFactory
from Factory import OutletProduct
from Factory import RegularProduct

customers_file = './customersfile.txt'
products_file = './productsfile.txt'
customers = Singleton.load_customers_from_csv(customers_file)
products = Singleton.load_products_from_csv(products_file)
DataLayer.write_customers_to_csv(customers, customers_file)
DataLayer.write_products_to_csv(products, products_file)
chosen_translations = ''


class product_management:
    global chosen_translations

    @staticmethod
    def create_product(product_type, item_id, name, description, price, quantity, currency='USD'):
        '''The function allows you to create new products based on the product type'''
        return ProductFactory.create_product(product_type, item_id, name, description, price, quantity, currency)

    def view_available_products(self):
        '''Shows the store's products'''
        for product in products:
            print(product)

    def view_all_customers(self):
        '''Shows all the customers of the store'''
        for customer in customers:
            print(customer)

    def add_regular_product(self, item_id, name, description, price, quantity):
        '''Adds a regular product'''
        return Product(item_id, name, description, price, quantity)

    def add_import_product(self, item_id, name, description, price, quantity):
        '''The function creates a new imported product based on the product details and additional information collected from the user'''
        source = input("Enter source country: \n")
        shipping_weeks = input("Enter shipping weeks time: \n")
        return ImportProduct(item_id, name, description, price, quantity, 'USA',
                             source, shipping_weeks)

    def add_outlet_product(self, item_id, name, description, price, quantity):
        '''The function creates a clearance sale product'''
        discount = input("Enter discount price: \n")
        return OutletProduct(item_id, name, description, price, quantity, 'USA',
                             discount)

    def update_existing_product(self):
        '''The function allows the user to update the details of an existing product in the product list.'''
        try:
            item_id = input(chosen_translations.get("please_enter_item_id_to_update:"))
            new_name = input(chosen_translations.get("please_enter_new_name:"))
            new_description = input(chosen_translations.get("please_enter_new_description:"))
            new_price = input(chosen_translations.get("please_enter_new_price:"))
            new_quantity = input(chosen_translations.get("please_enter_new_quantity:"))
            if not new_price.isdigit() or not new_quantity.isdigit():
                raise ValueError(chosen_translations.get("please_enter_valid_price_and_quantity")) # לבדוק אם זה קיים במילון
            new_price = float(new_price)
            new_quantity = int(new_quantity)

            if check_if_product_id_exists(item_id, products):
                new_product = Product(item_id, new_name, new_description, new_price, new_quantity)
                products[get_index_of_product(item_id, products)].__add__(new_name, new_description, new_price,
                                                                          new_quantity)
                print(f"{new_name}", chosen_translations.get("updated_successfully"))
            else:
                print(chosen_translations.get("item_id_is_exist_please_try_again"))

        except ValueError as ve:
            print(ve)

        except Exception as e:
            print(chosen_translations.get("an_error_occurred"), e)

    def remove_product(self):
        '''A function that removes a product'''
        item_id = input(chosen_translations.get("please_enter_item_id_to_remove:"))
        if check_if_product_id_exists(item_id, products):
            products.pop(get_index_of_product(item_id, products))
            print(f"{item_id}", chosen_translations.get("removed_successfully"))
        else:
            print(chosen_translations.get("item_id_is_not_exist,please_try_again"))


class Order_processing:
    def __init__(self, chosen_currency):
        self.chosen_currency = chosen_currency

    def pay_pal(self, attempts, products_oreders, current_customer, chosen_currency):
        '''A function that enables payment by PAYPAL and handles errors related to this payment method'''
        attempts = 0
        while attempts < 2:
            try:
                email = input(chosen_translations.get("enter_your_paypal_email_or_0_to_cancel:"))
                if email == "0":
                    print(chosen_translations.get("the_order_is_canceled"))
                    break

                password = input(chosen_translations.get("enter_your_paypal_password:"))
                matching_customer = None
                for customer in customers:
                    if customer.email == email:
                        matching_customer = customer
                        break

                if matching_customer is None:
                    print(chosen_translations.get("user_with_this_email_does_not_exist_Pleas_try_again"))
                    attempts += 1
                    continue

                if matching_customer.password != password:
                    print(chosen_translations.get("the_details_you_entered_are_incorrect_try_again"))
                    attempts += 1
                    continue

                print(chosen_translations.get("the_order_will_be_send_to_your_address_untill_5_days"))
                print(chosen_translations.get("thank_you_for_your_order_the_item:"))
                new_order = Order(products_oreders, current_customer, products)
                print(f"Your order number is: {new_order.order_id}")
                return new_order

            except Exception as e:
                print(f"An error occurred: {e}")
                attempts += 1

        print(chosen_translations.get("you_have_exceeded_the_maximum_number_of_attempts_Pleas_try_again_later"))
        return None

    def credit_cards(self, products_oreders, current_customer):
        ''''A function that allows payment by credit card and handles errors related to this payment method'''
        total_price = sum(int(products[get_index_of_product(item["item_id"], products)].price) * int(
            item["quantity"]) for item in products_oreders)
        while True:
            try:
                installment_option = int(input(chosen_translations.get("choose_installment_option_(1,2,3):")))
                if installment_option in [1, 2, 3]:
                    break
                print(chosen_translations.get("invalid_installment_option_pleas_try_again"))
            except ValueError:
                print(chosen_translations.get("invalid_installment_option_pleas_try_again"))

        installment_price = total_price / installment_option
        print(chosen_translations.get("each_installment_will_be:"),
              f"{installment_price} {self.chosen_currency}", chosen_translations.get("for_each"),
              f"{installment_option}", chosen_translations.get("month"))

        while True:
            card_number = input(chosen_translations.get("please_enter_your_16_digit_credit_card_number_or_0_to_cancel:"))
            if card_number == "0":
                print(chosen_translations.get("operation_canceled"))
                return None
            if card_number.isdigit() and len(card_number) == 16:
                break
            print(chosen_translations.get("invalid_input_Pleas_enter_a_16_digit_number"))

        while True:
            expiry_date = input(
                chosen_translations.get("please_enter_the_expiration_date_of_your_credit_card_(mm/yyyy)_or_0_to_cancel:"))
            if expiry_date == "0":
                print(chosen_translations.get("operation_canceled"))
                return None
            if expiry_date and PaymentProcessor.is_valid_expiry_date(expiry_date):
                print(chosen_translations.get("credit_card_expiration_date_is_valid"))
                break
            print(chosen_translations.get("invalid_input_Please_enter_a_valid_expiration_data"))

        while True:
            cvv = input(
                chosen_translations.get("please_enter_the_last_three_digits_on_the_back_of_the_card_or_0_to_cancel:"))
            if cvv == "0":
                print(chosen_translations.get("operation_canceled"))
                return None
            if cvv.isdigit() and len(cvv) == 3:
                break
            print(chosen_translations.get("invalid_input_please_enter_a_3_digit_number"))

        print(chosen_translations.get("ordered_successfully_the_receipt_will_be_sent_to"),
              f"{current_customer.email}")
        print(f"{current_customer.full_name}",
              chosen_translations.get("thank_you_for_your_order_the_order_will_delivery_to:"),
              f"{current_customer.address}")
        new_order = Order(products_oreders, current_customer, products)
        print(f"Your order number is: {new_order.order_id}")
        return new_order

    @staticmethod
    def is_valid_expiry_date(expiry_date):
        '''A function that checks the validity of the credit'''
        from datetime import datetime
        try:
            expiry = datetime.strptime(expiry_date, "%m/%Y")
            return expiry > datetime.now()
        except ValueError:
            return False

    def cash_on_delivery(self, product_order, current_customer):
        '''A function that allows cash payment to the courier and handles errors related to this payment method'''
        total_price = sum(
            int(products[get_index_of_product(item["item_id"], products)].price) * int(
                item["quantity"]) for item in product_order
        )
        print(chosen_translations.get("the_order_will_be_send_to_your_address_untill_5_days"))
        print(f"{current_customer.full_name}", chosen_translations.get(
            "thank_you_for_your_order_the_order_will_delivery_to:"),
              f"{current_customer.address}")
        new_order = Order(product_order, current_customer, products)
        print(f"Your order number is: {new_order.order_id}")
        return new_order

    def make_an_order(self, current_customer):
        '''A function that places an order and handles errors related to this payment method'''
        print(chosen_translations.get("this_is_the_list_of_product_for_purchase"))
        for product in products:
            print(product)
        product_order = []
        while True:
            total_price = 0
            print(chosen_translations.get("enter_0_in_item_id_to_stop"))
            item_id = input(chosen_translations.get("please_enter_item_id:"))
            if item_id == "0":
                print(chosen_translations.get("the_product_order_process_has_been_stopped"))
                order = Order(product_order, current_customer, products)
                total_price = order._calculate_total_price(products)
                print(chosen_translations.get("total_amount_to_be_charged:"), f"{total_price} {self.chosen_currency}",
                      chosen_translations.get("the_order_will_be_send_to_your_address_untill_5_days"))
                break

            elif get_index_of_product(item_id, products) == -1:
                print(chosen_translations.get("item_id_is_not_exist,please_try_again"))
                continue

            quantity = input(chosen_translations.get("please_enter_quantity:"))
            if not quantity.isdigit():
                print(chosen_translations.get("please_enter_valid_quantity"))
                continue

            quantity = int(quantity)
            if products[get_index_of_product(item_id, products)].quantity < quantity:
                print(chosen_translations.get("there_is_not_enough_quantity_of_this_product"))
                continue

            order = Order(product_order, current_customer, products)
            products[get_index_of_product(item_id, products)].quantity -= quantity
            product_order.append({"item_id": item_id, "quantity": quantity})
            print(f"{item_id}", chosen_translations.get("added_to_order_successfully"))
            total_price += product.price * quantity

        print('Your Cart:', product_order)
        if current_customer not in customers:
            youraddress = input(chosen_translations.get("please_enter_your_address:"))
        elif check_if_product_id_exists(item_id, products):
            for order in product_order:
                if order[chosen_translations.get("item_id")] == item_id:
                    order_quantity = int(order[chosen_translations.get("quantity")])
                    order_quantity += int(quantity)
                    break
                new_order = Order(product_order, current_customer, products)
                current_customer.orders.append(new_order)

        return product_order

    def view_order_history(self, orders):
        '''Prints the orders'''
        if len(orders) == 0:
            print(chosen_translations.get("looks_like_you_haven't_ordered_here_before"))
        else:
            for order in orders:
                print(order)

    def processing(self, orders, order_id):
        '''Updates shipping status for processing'''
        for order in orders:
            if order.order_id == order_id:
                order.update_status(chosen_translations.get("processing"))
                break

    def shipped(self, orders, order_id):
        '''Updates shipping status for shipped'''
        for order in orders:
            if order.order_id == order_id:
                order.update_status(chosen_translations.get("shipped"))
                break

    def delivered(self, orders, order_id):
        '''Updates shipping status for delivered'''
        for order in orders:
            if order.order_id == order_id:
                order.update_status(chosen_translations.get("delivered"))
                break

class Reporting:
    def total_revenue(self):
        '''The function calculates and displays the total revenue from all orders of all customers.'''
        total_sum = 0
        try:
            for customer in customers:
                for order in customer.orders:
                    total_sum += float(order.total_price)
            print(chosen_translations.get("total_revenues_is:"), f"{total_sum}")
        except ValueError as ve:
            print(chosen_translations.get("value_error_occurred"), ve)
        except KeyError as ke:
            print(chosen_translations.get("key_error_occurred"), ke)
        except Exception as e:
            print(chosen_translations.get("an_error_occurred"), e)

    def best_selling_product(self):
        '''The function returns the best-selling product'''
        try:
            total_sells = {}

            for customer in customers:
                for order in customer.orders:
                    for product in order.order_products:
                        item_id = product[chosen_translations.get("item_id")]
                        quantity = int(product[chosen_translations.get("quantity")])
                        total_sells[item_id] = total_sells.get(item_id, 0) + quantity

            if not total_sells:
                return

            best_seller_id = max(total_sells, key=total_sells.get)
            best_seller_val = total_sells[best_seller_id]
            best_seller_name = products[get_index_of_product(best_seller_id, products)].name

            print(chosen_translations.get("the_best_seller_(in_quantity)_is:"), f"{best_seller_id}",
                  chosen_translations.get("name"), f": {best_seller_name}",
                  chosen_translations.get("quantity"), f": {best_seller_val}")

        except KeyError as ke:
            print(chosen_translations.get("key_error_occurred"), ke)
        except ValueError as ve:
            print(chosen_translations.get("value_error_occurred"), ve)
        except Exception as e:
            print(chosen_translations.get("an_error_occurred"), e)

    def best_profitable_product(self):
        '''The function performed the calculation and printing of the most profitable product according to the revenues.'''
        try:
            total_sells = {}
            for customer in customers:
                for order in customer.orders:
                    for product in order.order_products:
                        item_id = product[chosen_translations.get("item_id")]
                        quantity = int(product[chosen_translations.get("quantity")])
                        product_price = int(products[get_index_of_product(item_id, products)].price)
                        total_sells[item_id] = total_sells.get(item_id, 0) + (quantity * product_price)
            if not total_sells:
                print(chosen_translations.get("no_sales_found"))
                return
            best_seller_id = max(total_sells, key=total_sells.get)
            best_seller_val = total_sells[best_seller_id]
            best_seller_name = products[get_index_of_product(best_seller_id, products)].name
            print(chosen_translations.get("the_best_profitable_(in_money)_is:"), f"{best_seller_id}",
                  chosen_translations.get("name"), f": {best_seller_name}",
                  chosen_translations.get("money"), f": {best_seller_val}")
        except KeyError as ke:
            print(chosen_translations.get("key_error_occurred"), ke)
        except ValueError as ve:
            print(chosen_translations.get("value_error_occurred"), ve)
        except Exception as e:
            print(chosen_translations.get("an_error_occurred"), e)


class User_registration:
    def __init__(self, logged_in):
        '''The function checks the client's connection and gives the possibility for a new client to register'''
        if logged_in[0]:  # user is not logged in
            print(chosen_translations.get("please_logout_and_then_try_to_register_new_customer"))
        else:
            fullname = input(chosen_translations.get("please_enter_full_name:"))
            id = input(chosen_translations.get("please_enter_id:"))
            password = input(chosen_translations.get("please_enter_password:"))
            phone = input(chosen_translations.get("please_enter_phone:"))
            while not phone.isdigit() or len(phone) != 10:
                print(chosen_translations.get(
                    "invalid_input_please_enter_a_10_digit_phone_number_containing_only_digits."))
                phone = input(chosen_translations.get("please_enter_phone_or_type_exit_to_quit:"))
                if phone.lower() == 'exit':
                    return None
            email = input(chosen_translations.get("please_enter_email:"))
            address = input(chosen_translations.get("please_enter_your_address,city_and_street"))
            if check_if_customer_id_exists(id, customers):
                print(chosen_translations.get("user_id_is_exists_pleas_try_something_different"))
            else:
                new_customer = Customer(full_name=fullname, id=id, password=password, phone=phone, email=email,
                                        address=address, is_admin=False)
                customers.append(new_customer)
                print(f"{fullname}", chosen_translations.get("registerd_successfully"))
                DataLayer.write_customers_to_csv(customers, customers_file)
                DataLayer.write_products_to_csv(products, products_file)


class Reviews:
    def add_review_and_rating_for_a_product(self, products, logged_in):
        '''The function deals with adding a review and rating to a certain product'''
        product_id = input(chosen_translations.get("enter_your_the_product_id:"))
        if check_if_product_id_exists(product_id, products):
            review_text = input(chosen_translations.get("enter_your_review:"))
            rating = input(chosen_translations.get("enter_your_rating(1-5):"))
            product = products[get_index_of_product(product_id, products)]
            product.add_review(logged_in[1], review_text, rating)
            print(chosen_translations.get("Review_added_successfully."))
        else:
            print(chosen_translations.get("product_id_does_not_exist."))

    def view_all_reviews_for_a_product(self, products):
        '''The function allows the user to view all reviews of a particular product in the system'''
        product_id = input(chosen_translations.get("enter_your_the_product_id:"))
        if check_if_product_id_exists(product_id, products):
            product = products[get_index_of_product(product_id, products)]
            product.__contains__()
        else:
            print(chosen_translations.get("product_id_does_not_exist."))


def main():
    from LanguageTranslator import LanguageTranslator
    translations_instance = None
    logged_in = [False, None]  # [state of logging | the user is logged in]
    chosen_currency = 'USD'
    print("1. English")
    print("2. Czech")
    print("3. Romanian")
    chosen_language = input("Please choose your language (English/Czech/Romanian): ").lower()
    while chosen_language.capitalize() not in ['English', 'Czech', 'Romanian', 'english', 'czech', 'romanian']:
        print("What you entered is invalid, please try again")
        chosen_language = input("Please choose your language (English/Czech/Romanian): ").lower()
    translations_instance = LanguageTranslator.get_translations()
    global chosen_translations
    chosen_translations = translations_instance.get(chosen_language)
    try:
        print(chosen_translations.get("Hello,welcome_to_our_furniture _store!"))
    except AttributeError:
        print("Translation not available for the chosen language.")
    if chosen_language == "Czech".lower().capitalize():
        chosen_currency = "CZK"
    if chosen_language == "Romanian".lower().capitalize():
        chosen_currency = "RON"
    else:
        chosen_currency = "USD"

    while True:
        print("1. ", chosen_translations.get("product_management"))
        print("2. ", chosen_translations.get("order_processing"))
        print("3. ", chosen_translations.get("reporting"))
        print("4. ", chosen_translations.get("user_registration"))
        print("5. ", chosen_translations.get("Logout") if logged_in[0] else chosen_translations.get("Login"))
        print("6. ", chosen_translations.get("reviews"))
        print("7. ", chosen_translations.get("exit"))

        primary_choice = input(chosen_translations.get("enter_your_choice_to_make"))
        if primary_choice == "1":
            if logged_in[0] and get_customer(logged_in, customers).is_admin:  # user is logged in and admin
                product_managemen = product_management()
                while True:
                    print("1. ", chosen_translations.get("view_available_products"))
                    print("2. ", chosen_translations.get("view_all_customers"))
                    print("3. ", chosen_translations.get("add_new_product"))
                    print("4. ", chosen_translations.get("update_existing_product"))
                    print("5. ", chosen_translations.get("remove_product"))
                    print("6. ", chosen_translations.get("exit"))
                    seconed_choice = input(chosen_translations.get("enter_your_choice_to_make"))
                    if seconed_choice == "1":
                        product_managemen.view_available_products()
                    elif seconed_choice == "2":
                        product_managemen.view_all_customers()
                    elif seconed_choice == "3":
                        while True:
                            print("1. Regular product")
                            print("2. Import product")
                            print("3. Outlet product")
                            print("4. Exit")
                            third_choice = input("Enter product type: \n")
                            if third_choice == '4':
                                break
                            item_id = input(chosen_translations.get("please_enter_item_id:"))
                            name = input(chosen_translations.get("please_enter_name:"))
                            description = input(chosen_translations.get("please_enter_description:"))
                            price = input(chosen_translations.get("please_enter_price:"))
                            while not price.isdigit():
                                price = input(chosen_translations.get("Please_enter_a_whole_number"))
                                if price.isdigit():
                                    break
                            quantity = input(chosen_translations.get("please_enter_quantity:"))
                            while not quantity.isdigit():
                                quantity = input(chosen_translations.get("Please_enter_a_whole_number"))
                            if check_if_product_id_exists(item_id, products):
                                print(chosen_translations.get("item_id_is_exist_please_try_again"))
                            else:
                                if third_choice == '1':
                                    new_product = product_managemen.add_regular_product(item_id, name, description,
                                                                                        price, quantity)
                                if third_choice == '2':
                                    new_product = product_managemen.add_import_product(item_id, name, description,
                                                                                       price, quantity)
                                if third_choice == '3':
                                    new_product = product_managemen.add_outlet_product(item_id, name, description,
                                                                                       price, quantity)
                                products.append(new_product)
                                print(f"{name}", chosen_translations.get("added_successfully"))
                    elif seconed_choice == "4":
                        product_managemen.update_existing_product()
                    elif seconed_choice == "5":
                        product_managemen.remove_product()
                    elif seconed_choice == "6":
                        break
                    else:
                        print(chosen_translations.get("try_again_arror_in_choice"))
            else:
                print(chosen_translations.get(
                    "you_are_not_logged_in_to_system_or_and_you_are_not_admin_manager_of_store"))

        elif primary_choice == "2":
            if logged_in[0]:  # user is logged in
                while True:
                    print("1. ", chosen_translations.get("make_an_order"))
                    print("2. ", chosen_translations.get("view_order_history"))
                    print("3. ", chosen_translations.get("update_order_status"))
                    print("4, ", chosen_translations.get("exit"))
                    seconed_choice = input(chosen_translations.get("enter_your_choice_to_make"))
                    order_processing = Order_processing(chosen_currency)
                    current_customer = get_customer(logged_in, customers)
                    if seconed_choice == "1":
                        products_oreders = order_processing.make_an_order(current_customer)
                        print("1. ", chosen_translations.get("pay_pal"))
                        print("2. ", chosen_translations.get("credit_cards"))
                        print("3. ", chosen_translations.get("cash_on_delivery"))
                        attempts = 0
                        payment_method = input(chosen_translations.get("please_choose_payment_method:"))
                        total_price = sum(int(products[get_index_of_product(item["item_id"], products)].price) * int(
                            item["quantity"]) for item in products_oreders)
                        print(chosen_translations.get("total_amount_to be_charged:"),
                              f"{total_price} {chosen_currency}")
                        if payment_method == "1":
                            order_processing = Order_processing(chosen_currency)
                            new_order = order_processing.pay_pal(attempts, products_oreders, current_customer, chosen_currency)
                            current_customer.orders.append(new_order)
                        elif payment_method == "2":
                            new_order = order_processing.credit_cards(products_oreders, current_customer)
                            current_customer.orders.append(new_order)
                        elif payment_method == "3":
                            new_order = order_processing.cash_on_delivery(products_oreders, current_customer)
                            current_customer.orders.append(new_order)

                    elif seconed_choice == "2":
                        order_processing.view_order_history(current_customer.orders)
                    elif seconed_choice == "3":
                        if logged_in[0] and get_customer(logged_in, customers).is_admin:
                            order_id = input(chosen_translations.get("enter_order_id_to_update:"))
                            if check_if_order_id_exists(current_customer.orders, order_id):
                                print(chosen_translations.get("Now_,_choose_new_status"))
                                print("1. ", chosen_translations.get("processing"))
                                print("2. ", chosen_translations.get("shipped"))
                                print("3. ", chosen_translations.get("delivered"))
                                status_choice = input(chosen_translations.get("enter_status_to_update:"))
                                if status_choice == "1":
                                    order_processing.processing(current_customer.orders, order_id)
                                    print(chosen_translations.get("update_order_status_success"))
                                elif status_choice == "2":
                                    order_processing.shipped(current_customer.orders, order_id)
                                    print(chosen_translations.get("update_order_status_success"))
                                elif status_choice == "3":
                                    order_processing.delivered(current_customer.orders, order_id)
                                    print(chosen_translations.get("update_order_status_success"))
                                else:
                                    print(chosen_translations.get("try_again_error_in_choice"))
                            else:
                                print(chosen_translations.get("order_id_is_not_exist"))
                        else:
                            print(chosen_translations.get("only_administrators_can_update_shipping_status"))

                    if seconed_choice == "4":
                        break
                    else:
                        print(chosen_translations.get("try_again_error_in_choice"))
                else:
                    print(chosen_translations.get("you_are_not_logged_in_to_system"))

        if primary_choice == "3":
            if logged_in[0] and get_customer(logged_in, customers).is_admin:  # user is logged in and admin
                reporting = Reporting()
                while True:
                    print("1. ", chosen_translations.get("total_revenue"))
                    print("2. ", chosen_translations.get("best_selling_product"))
                    print("3. ", chosen_translations.get("best_profitable_product"))
                    print("4. ", chosen_translations.get("exit"))
                    report_choice = input(chosen_translations.get("enter_your_choice_to_make"))
                    if report_choice == "1":
                        reporting.total_revenue()
                    if report_choice == "2":
                        reporting.best_selling_product()
                    if report_choice == "3":
                        reporting.best_profitable_product()
                    if report_choice == "4":
                        break
            else:
                print(chosen_translations.get(
                    "you_are_not_logged_in_to_system_or/and_you_are_not_admin_manager_of_store"))

        elif primary_choice == "4":
            user_registration = User_registration(logged_in)

        elif primary_choice == "5":
            if logged_in[0]:
                print(chosen_translations.get("bye_bye!"))
                logged_in = [False, None]
            else:
                id = input(chosen_translations.get("please_enter_id:"))
                password = input(chosen_translations.get("please_enter_password:"))
                try_login = login(id, password, customers)
                if try_login:
                    print(chosen_translations.get("welcome,you_are_logged_in_now!"))
                    logged_in = [True, id]
                else:
                    print(chosen_translations.get("wrong_details,pleas_try_again!"))

        elif primary_choice == "6":
            if logged_in[0]:  # user is logged in
                reviews = Reviews()
                while True:
                    print("1. ", chosen_translations.get("add_review_and_rating_for_a_product"))
                    print("2. ", chosen_translations.get("view_all_reviews_for_a_product"))
                    print("3. ", chosen_translations.get("exit"))
                    review_choice = input(chosen_translations.get("enter_your_choice_to_make"))
                    if review_choice == "1":
                        reviews.add_review_and_rating_for_a_product(products, logged_in)
                    elif review_choice == "2":
                        reviews.view_all_reviews_for_a_product(products)
                    elif review_choice == "3":
                        break
                    else:
                        print(chosen_translations.get("invalid_choice.Please_try_again"))

        if primary_choice == "7":
            print(chosen_translations.get("thank_you_for_using_our_system"))
            break


main()