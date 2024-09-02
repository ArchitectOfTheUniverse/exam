import json
from datetime import datetime, date
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
    def __init__(self, id, producer, model, release_date,
                 cost, potential_sale_price):
        self.id = id
        self.producer = producer
        self.model = model
        self.release_date = release_date
        self.cost = cost
        self.potential_sale_price = potential_sale_price

    def __repr__(self):
        return (f"Car - {self.id} - {self.producer} - {self.model}, "
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
    def load_from_file(self, filename):
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
    def save_to_file(self, data, filename):
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
        self.cars[car.id] = car

    def remove_car(self, car_id):
        if car_id in self.cars:
            del self.cars[car_id]

    def register_sale(self, employee_id, car_id, sale_date, real_sale_price):
        today = datetime.now().date()
        date_obj = datetime.strptime(sale_date, "%Y-%m-%d").date()
        if date_obj > today:
            print("Sale date is in the future")
            return None

        if employee_id in self.employees and car_id in self.cars:
            sale = Sale(self.employees[employee_id], self.cars[car_id], sale_date, real_sale_price)
            self.sales.append(sale)
            del self.cars[car_id]
            return sale
        else:
            print(f"Employee - {employee_id} "
                  f"or Car - {car_id} not found")
            return None

    def get_most_sale_car(self, start_date, end_date):
        sales_in_period = [sale for sale in self.sales if
                           start_date <= sale.sale_date <= end_date]
        if not sales_in_period:
            return "No sales in this period"
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
        total_sales_cost = sum(sale.car.cost for sale in sales_in_period)
        real_prices = sum(sale.real_sale_price for sale in sales_in_period)
        total_profit = real_prices - total_sales_cost
        return total_profit

    def generate_reports(self, report, date=None, start_date=None,
                         end_date=None, employee_id=None):
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
            return list(self.employees.values())
        elif report == 'show_cars':
            return list(self.cars.values())
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
            return data
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
    SHOW_SALES_IN_PERIOD = auto()
    SHOW_SALES_BY_EMPLOYEE = auto()
    SHOW_MOST_SALE_CAR_IN_PERIOD = auto()
    SHOW_TOP_EMPLOYEE_IN_PERIOD = auto()
    SHOW_PROFIT_IN_PERIOD = auto()
    BACK = auto()


class AutoSalonMenu:
    def __init__(self, salon):
        self.salon = salon

    def main_menu(self):
        print("Main Menu!")
        for item in Menu:
            print(f"{item.value}. {item.name.replace('_', ' ').title()}")


    def reports_menu(self):
        print("Reports Menu!")
        for item in ReportsMenu:
            print(f"{item.value}. {item.name.replace('_', ' ').title()}")

    def start(self):
        while True:
            self.main_menu()
            choice = int(input("Make your choice: >> "))
            menu_choice = Menu(choice)

            if menu_choice == Menu.ADD_EMPLOYEE:
                self.add_employee()
            elif menu_choice == Menu.REMOVE_EMPLOYEE:
                self.remove_employee()
            elif menu_choice == Menu.ADD_CAR:
                self.add_car()
            elif menu_choice == Menu.REMOVE_CAR:
                self.remove_car()
            elif menu_choice == Menu.REGISTER_SALE:
                self.register_sale()
            elif menu_choice == Menu.SHOW_REPORTS:
                self.show_reports()
            elif menu_choice == Menu.EXIT:
                print("Quiting the program")
                break

    def add_employee(self):
        id = input("Enter employee id "
                   "(ID must be an integer): >> ")
        full_name = input("Enter first and last "
                          "name separated by a space: >> ").title()
        position = input("Enter the position of the employee: >> ").title()
        phone_number = input("Enter phone number of the employee: >> ")
        email = input("Enter email of the employee: >> ")
        employee = Employee(id, full_name, position, phone_number, email)
        self.salon.add_employee(employee)
        print("Employee added!")

    def remove_employee(self):
        id = input("Enter employee id "
                   "(ID must be an integer: >> ")
        self.salon.remove_employee(id)
        print("Employee removed!")

    def add_car(self):
        id = input("Enter car id "
                   "(ID must be an snteger): >> ")
        producer = input("Enter the name of the manufacturer: >> ").title()
        model = input("Enter the name of the model: >> ").title()
        release_date = input(
            "Enter the release date in format YYYY MM DD"
        ).replace(" ","-")
        cost = input("Enter the cost of the car: >> ")
        potential_sale_price = input(
            "Enter the potential sale price of the car: >> "
        )
        car = Car(id, producer, model, release_date, cost, potential_sale_price)
        self.salon.add_car(car)
        print("Car added!")

    def remove_car(self):
        id = input("Enter car id "
                   "(ID must be an integer): >> ")
        self.salon.remove_car(id)
        print("Car removed!")

    def register_sale(self):
        employee_id = input("Enter employee id "
                            "(ID must be an integer): >> ")
        car_id = input("Enter car id "
                       "(ID must be an integer): >> ")
        sale_date = input("Enter date of "
                          "sale in format "
                          "YYYY MM DD: >> ").replace(" ", "-")
        real_sale_price = input("Enter real sale price of the car "
                                "(Must consist only of "
                                "numbers without spaces): >> ")
        self.salon.register_sale(employee_id, car_id, sale_date, real_sale_price)
        print("Registration successful!")

    def show_reports(self):
        while True:
            self.reports_menu()
            choice = int(input("Make your choice: >> "))
            report_choice = ReportsMenu(choice)

            if report_choice == ReportsMenu.SHOW_EMPLOYEES:
                items = self.salon.generate_reports("show_employees")
                self.salon.display_or_save_report(items)
            elif report_choice == ReportsMenu.SHOW_CARS:
                items = self.salon.generate_reports("show_cars")
                self.salon.display_or_save_report(items)
            elif report_choice == ReportsMenu.SHOW_REPORTS_BY_DATE:
                search_date = input(
                    "Enter the start date in format YYYY MM DD: >> "
                ).replace(" ", " ")
                sales_by_date = self.salon.generate_reports_by_date("sales_by_date"
                                                                    , date=search_date)
                self.salon.display_or_save_report(sales_by_date)
            elif report_choice == ReportsMenu.SHOW_SALES_IN_PERIOD:
                start_date = input("Enter the start date "
                                   "in format YYYY MM DD: >> ").replace(" ", "-")
                end_date = input(
                    "Enter the end date in format YYYY MM DD: >> "
                ).replace(" ", "-")
                items = self.salon.generate_reports("sales_in_period",
                                                              start_date=start_date, end_date=end_date)
                self.salon.display_or_save_report(items)
            elif report_choice == ReportsMenu.SHOW_SALES_BY_EMPLOYEE:
                employee_id = input("Enter employee id(ID must be an integer): >> ")
                items = self.salon.generate_reports("sales_by_employee", employee_id=employee_id)
                self.salon.display_or_save_report(items)
            elif report_choice == ReportsMenu.SHOW_MOST_SALE_CAR_IN_PERIOD:
                start_date = input("Enter the start date "
                                   "in format YYYY MM DD: >> ").replace(" ", "-")
                end_date = input(
                    "Enter the end date in format YYYY MM DD: >> "
                ).replace(" ", "-")
                items = self.salon.generate_reports("top_sale_car",
                                                           start_date=start_date, end_date=end_date)
                self.salon.display_or_save_report(items)
            elif report_choice == ReportsMenu.SHOW_TOP_EMPLOYEE_IN_PERIOD:
                start_date = input("Enter the start date "
                                   "in format YYYY MM DD: >> ").replace(" ", "-")
                end_date = input(
                    "Enter the end date in format YYYY MM DD: >> "
                ).replace(" ", "-")
                items = self.salon.generate_reports("top_employee",
                                                           start_date=start_date, end_date=end_date)
                self.salon.display_or_save_report(items)
            elif report_choice == ReportsMenu.SHOW_PROFIT_IN_PERIOD:
                start_date = input("Enter the start date "
                                   "in format YYYY MM DD: >> ").replace(" ", "-")
                end_date = input(
                    "Enter the end date in format YYYY MM DD: >> "
                ).replace(" ", "-")
                items = self.salon.generate_reports("profit_in_period",
                                                               start_date=start_date, end_date=end_date)
                self.salon.display_or_save_report(items)
            elif report_choice == ReportsMenu.BACK:
                break
            else:
                print("Invalid choice")
                continue

            for item in items:
                print(item)

if __name__ == "__main__":
    salon = AutoSalon()
    menu = AutoSalonMenu(salon)
    menu.start()





















































































































































