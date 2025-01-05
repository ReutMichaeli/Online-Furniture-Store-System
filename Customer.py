from abc import ABC, abstractmethod
import csv
from Product import Product
from ImportProduct import ImportProduct

class Customer:
    def __init__(self, full_name, id, password, phone, email, address, is_admin):
        '''data initialization'''
        self.full_name = full_name
        self.id = id
        self.password = password
        self.phone = phone
        self.email = email
        self.address = address
        self.is_admin = is_admin
        self.orders = []

    def update_order(self, order_id, new_status):
        '''Updates the status of a particular order for a customer by order ID'''
        for order in self.orders:
            if int(order.order_id) == int(order_id):
                order.update_status(new_status)

    def __str__(self):
        return f"full name: {self.full_name}, id: {self.id}, password: ****** :), phone: {self.phone}, email: {self.email}, admin: {self.is_admin}"