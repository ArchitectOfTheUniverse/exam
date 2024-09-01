import json
from datetime import datetime
from enum import Enum, auto
from collections import Counter


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


class LoadDataFromFile:
    def load_from_file(self,filename):
        try:
            with open(filename, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"File {filename} not found")
            return None
        except Exception as e:
            print(f"Error loading file: {e}")
            return None


class SaveDataToFile:
    def save_to_file(self,data, filename):
        try:
            with open(filename, "w") as file:
                json.dump(data, file, default=str, indent=4)
        except Exception as e:
            print(f"Error saving file: {e}")


class AutoSalon:
    def __init__(self):
        self.open_file = LoadDataFromFile()
        self.save_file = SaveDataToFile()
        self.employees = {}
        self.cars = {}
        self.sales = []

    def add_employee(self, employee: Employee):
        self.employees[employee.id] = employee

    def remove_employee(self, employee_id):
        if employee_id in self.employees:
            del self.employees[employee_id]

    def add_car(self, car: Car):
        self.cars[car.model] = car

    def remove_car(self, car_model):
        if car_model in self.cars:
            del self.cars[car_model]

    def register_sale(self, employee_id, car_model, sale_date, real_sale_price):
        today = datetime.now().date()
        date_obj = datetime.strptime(sale_date, "%Y-%m-%d").date()
        if date_obj > today:
            print("Sale date is in the future")
            return None

        if employee_id in self.employees and car_model in self.cars:
            sale = Sale(self.employees[employee_id], self.cars[car_model], sale_date, real_sale_price)
            self.sales.append(sale)
            del self.cars[car_model]
            return sale
        else:
            print(f"Employee - {employee_id} "
                  f"or Car - {car_model} not found")
            return None

    def get_most_sale_car(self, start_date, end_date):
        sales_in_period = [sale for sale in self.sales if
                           start_date <= sale.sale_date <= end_date]
        if not sales_in_period:
            return "Na sales in this period"
        models_sale = [sale.car.model for sale in sales_in_period]
        most_sale_car = Counter(models_sale).most_common(1)[0][0]
        return f"The most sale car is {most_sale_car}"

    def get_top_employee(self, start_date, end_date):
        sales_in_period = [sale for sale in self.sales if
                           start_date <= sale.sale_date <= end_date]
        if not sales_in_period:
            return "Na sales in this period"
        employees_sale = Counter([sale.employee.full_name for sale in sales_in_period])
        top_employee = employees_sale.most_common(1)[0][0]
        return f"The top employee is {top_employee}"

    def get_total_profit(self, start_date, end_date):
        sales_in_period = [sale for sale in self.sales if
                           start_date <= sale.sale_date <= end_date]
        total_profit = sum(sale.real_sale_price - sale.car.cost for sale in sales_in_period)
        return f"The total profit is {total_profit}"

    def generate_reports(self, report, date=None, start_date=None,
                         end_date=None, employee_id=None):
        today = datetime.now().date()
        date_obj = datetime.strptime(date, "%Y-%m-%d").date()
        if date_obj > today:
            print("Sale date is in the future")
            return []

        if report == 'all_sales':
            return self.sales
        elif report == 'sales_by_period':
            return [sale for sale in self.sales if
                    start_date <= sale.sale_date <= end_date]
        elif report == 'sales_by_employee':
            return [sale for sale in self.sales if
                    sale.employee.id == employee_id]
        elif report == 'sales_by_date':
            return [sale for sale in self.sales if
                    sale.sale_date == date]
        elif report == 'show_employees':
            return self.employees
        elif report == 'show_cars':
            return self.cars
        elif report == 'most_sale_car':
            return self.get_most_sale_car(start_date, end_date)
        elif report == 'top_employee':
            return self.get_top_employee(start_date, end_date)
        elif report == 'total_profit':
            return self.get_total_profit(start_date, end_date)

    def display_or_save_report(self, data):
        choice = input("Would you like to Display(1) or Save(2) "
                       "report? Enter 1 or 2: >> ")
        if choice == '1':
            print("\n".join(data))
        elif choice == '2':
            filename = input("Enter filename to save the report: >> ")
            self.save_file.save_to_file(data, filename)
            print(f"Report saved to {filename}")


class Menu(Enum):
    ADD_EMPLOYEE = auto()
    REMOVE_EMPLOYEE = auto()
    ADD_CAR = auto()
    REMOVE_CAR = auto()
    REGISTER_SALE = auto()
    SHOW_REPORTS = auto()
    EXIT = auto()


class ReportsMenu(Enum):
    SHOW_EMPLOYEES = auto()
    SHOW_CARS = auto()
    SHOW_SALES = auto()
    SHOW_REPORTS_BY_DATE = auto()
    SHOW_REPORTS_IN_PERIOD = auto()
    SHOW_REPORTS_BY_EMPLOYEE = auto()
    SHOW_MOST_SALE_CAR_IN_PERIOD = auto()
    SHOW_TOP_EMPLOYEE_IN_PERIOD = auto()
    SHOW_PROFIT_IN_PERIOD = auto()
    BACK = auto()





























































































































































