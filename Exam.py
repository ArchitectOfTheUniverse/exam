import json
from datetime import datetime
from enum import Enum, auto


class Employee:
    def __init__(self, id_number, full_name, position,
                 phone_number, email):
        self.id = id_number
        self.full_name = full_name
        self.position = position
        self.phone_number = phone_number
        self.email = email

    def __repr__(self):
        return (f"Employee - {self.full_name}, ID - {self.id}, "
                f"Position - {self.position}, "
                f"Phone Number - {self.phone_number}, "
                f"Email - {self.email}")


class Car:
    def __init__(self, producer, model, release_date,
                 cost, potential_sale_price):
        self.producer = producer
        self.model = model
        self.release_date = release_date
        self.cost = cost
        self.potential_sale_price = potential_sale_price

    def __repr__(self):
        return (f"Car - {self.producer} - {self.model}, "
                f"Release - {self.release_date}, "
                f"Cost - {self.cost}, "
                f"Potential Sale Price - {self.potential_sale_price}")


class Sale:
    def __init__(self, employee: Employee, car: Car, sale_date, real_sale_price):
        self.employee = employee
        self.car = car
        self.sale_date = sale_date
        self.real_sale_price = real_sale_price

    def __repr__(self):
        return (f"Sale {self.car} by {self.employee}, "
                f"on {self.sale_date} for {self.real_sale_price}")











































































































































