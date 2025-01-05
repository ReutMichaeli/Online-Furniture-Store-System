import csv
from Customer import Customer
from Product import Product
from abc import ABC, abstractmethod


class DataLayer(ABC):
    @abstractmethod
    def load_customers_from_csv(customers):
        '''A static function whose purpose is to load customer data from a CSV file and return a list of customer objects'''
        customers = []
        with open('./customersfile.txt', mode='r', newline='',
                  encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                customers.append(Customer(row['full_name'], row['id'], row['password'], row['phone'], row['email'],
                                          row['address'], row['is_admin']))
        return customers

    @abstractmethod
    def load_products_from_csv(products):
        '''A static function whose purpose is to load product data from a CSV file and return a list of product objects'''
        products = []
        with open('./productsfile.txt', mode='r', newline='', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                products.append(
                    Product(row['item_id'], row['name'], row['description'], row['price'], row['quantity'],
                            row['currency']))
        return products

    @abstractmethod
    def write_customers_to_csv(customers, customersfile):
        '''A static function whose purpose is to write customer data to a CSV file on the computer.'''
        with open(customersfile, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['full_name', 'id', 'password', 'phone', 'email', 'address', 'is_admin'])
            for customer in customers:
                writer.writerow([customer.full_name, customer.id, customer.password, customer.phone, customer.email,
                                 customer.address, customer.is_admin])

    @abstractmethod
    def customers(self, customers):
        '''The function is used to write customer data to a CSV file'''
        with open(self.customers_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['full_name', 'id', 'password', 'phone', 'email', 'address', 'is_admin'])
            for customer in customers:
                writer.writerow([customer.full_name, customer.id, customer.password, customer.phone, customer.email,
                                 customer.address, customer.is_admin])

    @abstractmethod
    def write_products_to_csv(products, productsfile):
        '''The function writes product data to a CSV file'''
        with open(productsfile, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['item_id', 'name', 'description', 'price', 'quantity', 'currency'])
            for product in products:
                writer.writerow(
                    [product.item_id, product.name, product.description, product.price, product.quantity,
                     product.currency])

