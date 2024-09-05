import pickle
from datetime import datetime
from collections import Counter
from enum import Enum, auto


class Employee:
    def __init__(self, employee_id, full_name, position, phone_number, email):
        self.employee_id = employee_id
        self.full_name = full_name
        self.position = position
        self.phone_number = phone_number
        self.email = email

    def __repr__(self):
        return (f"Employee: ID - {self.employee_id}, Full name - {self.full_name}, "
                f"Position - {self.position}, Phone number - {self.phone_number}, "
                f"Email - {self.email}")


class Car:
    def __init__(self, car_id, producer, model,
                 release_year, cost, potential_sale_price):
        self.car_id = car_id
        self.producer = producer
        self.model = model
        self.release_year = release_year
        self.cost = cost
        self.potential_sale_price = potential_sale_price

    def __repr__(self):
        return (f"Car: ID - {self.car_id}, Producer - {self.producer}, "
                f"Model - {self.model}, Release year - {self.release_year}, "
                f"Cost - {self.cost}, "
                f"Potential sale price - {self.potential_sale_price}")


class Sale:
    def __init__(self, employee: Employee, car: Car,
                 sale_date, real_sale_price):
        self.employee = employee
        self.car = car
        self.sale_date = sale_date
        self.real_sale_price = real_sale_price

    def __repr__(self):
        return (f"Sale: Employee - {self.employee.employee_id}, Car - {self.car}, "
                f"Sale date - {self.sale_date}, "
                f"Real sale price - {self.real_sale_price}")


class SaveDataToFile:
    @staticmethod
    def save_data_to_file(data, filename):
        try:
            with open(filename, 'wb') as file:
                pickle.dump(data, file)
                print(f"Data saved to {filename}")
        except Exception as e:
            print(f"Error saving file {filename}: {e}")


class LoadDataFromFile:
    @staticmethod
    def load_data_from_file(filename):
        try:
            with open(filename, 'rb') as file:
                data = pickle.load(file)
                print("Data loaded from file")
                return data
        except FileNotFoundError:
            print(f"File {filename} not found")
            return None
        except Exception as e:
            print(f"Error loading file {filename}: {e}")
            return None


class DateValidator:
    @staticmethod
    def validate_date(input_date):
        try:
            if input_date > datetime.now():
                print("Date entered is in the future")
                return None
            return input_date
        except ValueError:
            print("Date entered is not in the correct format. "
                  "Enter date in format (YYYY-MM-DD)")
            return None


class AutoSalon:
    def __init__(self):
        self.employees = {}
        self.cars = {}
        self.sales = []

    def add_employee(self, employee: Employee):
        self.employees[employee.employee_id] = employee

    def remove_employee(self, employee: Employee):
        if employee.employee_id in self.employees:
            del self.employees[employee.employee_id]

    def add_car(self, car: Car):
        self.cars[car.car_id] = car

    def remove_car(self, car: Car):
        if car.car_id in self.cars:
            del self.cars[car.car_id]

    def register_sale(self, employee_id, car_id, sale_date, real_sale_price):
        if employee_id not in self.employees or car_id not in self.cars:
            print(f"Employee - {employee_id} or car - {car_id} not found")
            return None

        sale = Sale(self.employees[employee_id], self.cars[car_id],
                    sale_date, real_sale_price)
        self.sales.append(sale)
        del self.cars[car_id]
        print("Sale registered")
        return sale

    def save_data(self, filename):
        data = {"employees": self.employees, "cars": self.cars, "sales": self.sales}
        SaveDataToFile.save_data_to_file(data, filename)


    def load_data(self, filename):
        data = LoadDataFromFile.load_data_from_file(filename)
        if data:
            self.employees = data.get("employees", {})
            self.cars = data.get("cars", {})
            self.sales = data.get("sales", [])
            print("Data loaded")


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


class ReportGenerator:
    def __init__(self, salon: AutoSalon):
        self.salon = salon

    def generate_report(self, report_type: ReportsMenu, date=None,
                        start_date=None, end_date=None, employee_id=None):
        if report_type == ReportsMenu.SHOW_EMPLOYEES:
            return list(self.salon.employees.values())
        elif report_type == ReportsMenu.SHOW_CARS:
            return list(self.salon.cars.values())
        elif report_type == ReportsMenu.SHOW_SALES:
            return self.salon.sales
        elif report_type == ReportsMenu.SHOW_REPORTS_BY_DATE:
            return [sale for sale in self.salon.sales
                    if sale.sale_date == date]
        elif report_type == ReportsMenu.SHOW_SALES_IN_PERIOD:
            return [sale for sale in self.salon.sales
                    if start_date <= sale.sale_date <= end_date]
        elif report_type == ReportsMenu.SHOW_SALES_BY_EMPLOYEE:
            return [sale for sale in self.salon.sales
                    if sale.employee.employee_id == employee_id]
        elif report_type == ReportsMenu.SHOW_MOST_SALE_CAR_IN_PERIOD:
            return self.get_most_sale_car(start_date, end_date)
        elif report_type == ReportsMenu.SHOW_TOP_EMPLOYEE_IN_PERIOD:
            return self.get_top_employee(start_date, end_date)
        elif report_type == ReportsMenu.SHOW_PROFIT_IN_PERIOD:
            return self.get_total_profit(start_date, end_date)

    def get_most_sale_car(self, start_date, end_date):
        sales_in_period = [sale for sale in self.salon.sales
                           if start_date <= sale.sale_date <= end_date]
        if not sales_in_period:
            return "No sales in period"

        cars = [sale.car.model for sale in sales_in_period]
        most_sale_car = Counter(cars).most_common(1)[0][0]
        return f"Most sale car in period - {most_sale_car}"

    def get_top_employee(self, start_date, end_date):
        sales_in_period = [sale for sale in self.salon.sales
                           if start_date <= sale.sale_date <= end_date]
        if not sales_in_period:
            return "No sales in period"

        employee_sales = Counter([sale.employee.full_name for sale
                                  in sales_in_period])
        top_employee = employee_sales.most_common(1)[0][0]
        return f"The top employee is {top_employee}"

    def get_total_profit(self, start_date, end_date):
        sales_in_period = [sale for sale in self.salon.sales
                           if start_date <= sale.sale_date <= end_date]
        if not sales_in_period:
            return "No sales in period"

        total_profit = sum(float(sale.real_sale_price) - float(sale.car.cost)
                           for sale in sales_in_period)
        return f"Total profit in period is: {total_profit}"


class ReportProcessor:
    def __init__(self, report_generator: ReportGenerator):
        self.report_generator = report_generator

    def display_or_save_report(self, report_type: ReportsMenu, **kwargs):
        report = self.report_generator.generate_report(report_type, **kwargs)
        choice = input(
            "Would you like to Display(1) or Save(2) "
            "report? Enter 1 or 2: >> "
        )

        if choice == "1":
            print(report)
        elif choice == "2":
            filename = input("Enter filename to save report")
            SaveDataToFile.save_data_to_file(report, filename)
        else:
            print("Invalid choice")


class Menu(Enum):
    ADD_EMPLOYEE = auto()
    REMOVE_EMPLOYEE = auto()
    ADD_CAR = auto()
    REMOVE_CAR = auto()
    REGISTER_SALE = auto()
    SHOW_REPORTS = auto()
    SAVE_DATA = auto()
    LOAD_DATA = auto()
    EXIT = auto()


class AutoSalonMenu:
    def __init__(self, salon):
        self.salon = salon
        self.report_generator = ReportGenerator(salon)
        self.report_processor = ReportProcessor(self.report_generator)

    def main_menu(self):
        print("Main menu:")
        for menus in Menu:
            print(f"{menus.value}. "
                  f"{menus.name.replace("_", " ").title()}")

    def reports_menu(self):
        print("Reports menu:")
        print("1. Show employees\n"
              "2. Show cars\n"
              "3. Show sales\n"
              "4. Show reports by date\n"
              "5. Show sales in period\n"
              "6. Show sales by employee\n"
              "7. Show most sale car\n"
              "8. Show top employee in period\n"
              "9. Show profit in period\n"
              "10. Back to main menu")

    def start(self):
        while True:
            self.main_menu()
            choice = int(input("Make your choice: >> "))
            if choice == Menu.ADD_EMPLOYEE.value:
                self.add_employee()
            elif choice == Menu.REMOVE_EMPLOYEE.value:
                self.remove_employee()
            elif choice == Menu.ADD_CAR.value:
                self.add_car()
            elif choice == Menu.REMOVE_CAR.value:
                self.remove_car()
            elif choice == Menu.REGISTER_SALE.value:
                self.register_sale()
            elif choice == Menu.SHOW_REPORTS.value:
                self.show_reports()
            elif choice == Menu.SAVE_DATA.value:
                self.save_data()
            elif choice == Menu.LOAD_DATA.value:
                self.load_data()
            elif choice == Menu.EXIT.value:
                print("Exit")
                break
            else:
                print("Invalid choice")

    def add_employee(self):
        employee_id = input(
            "Enter employee ID "
            "(ID must be an integer): >> "
        )
        full_name = input(
            "Enter first and last name separated by a space: >> "
        ).title()
        position = input(
            "Enter employee position: >> "
        ).title()
        phone_number = input(
            "The number must contain only numbers"
        )
        email = input(
            "Enter employee email: >> "
        )

        employee = Employee(employee_id, full_name, position,
                            phone_number, email)
        self.salon.add_employee(employee)
        print(f"Employee {employee} added")

    def remove_employee(self):
        employee_id = input(
            "Enter employee ID "
            "(ID must be an integer): >> "
        )

        self.salon.remove_employee(employee_id)
        print(f"Employee {employee_id} removed")

    def add_car(self):
        car_id = input(
            "Enter car ID "
            "(ID must be an integer): >> "
        )
        producer = input(
            "Enter car producer: >> "
        ).title()
        model = input(
            "Enter car model: >> "
        ).title()
        release_year = input(
            "Enter car release year: >> "
        )
        cost = float(input(
            "Enter car cost: >> "
        ))
        potential_sale_price = float(input(
            "Enter car potential sale price: >> "
        ))

        car = Car(car_id, producer, model, release_year,
                  cost, potential_sale_price)
        self.salon.add_car(car)
        print(f"Car {car} added")

    def remove_car(self):
        car_id = input(
            "Enter car ID "
            "(ID must be an integer): >> "
        )
        self.salon.remove_car(car_id)
        print(f"Car {car_id} removed")

    def register_sale(self):
        employee_id = input(
            "Enter employee ID "
            "(ID must be an integer): >> "
        )
        car_id = input(
            "Enter car ID "
            "(ID must be an integer): >> "
        )
        sale_date = datetime.strptime(input(
            "Enter date of sale "
            "in format (YYYY-MM-DD): >> "
        ), "%Y-%m-%d")
        real_sale_price = float(input(
            "Enter real sale price: >> "
        ))

        self.salon.register_sale(employee_id, car_id, sale_date, real_sale_price)

    def show_reports(self):
        while True:
            self.reports_menu()
            choice = input("Make your choice: >> ")
            if choice == '1':
                self.report_processor.display_or_save_report(
                    ReportsMenu.SHOW_EMPLOYEES
                )
            elif choice == '2':
                self.report_processor.display_or_save_report(
                    ReportsMenu.SHOW_CARS
                )
            elif choice == '3':
                self.report_processor.display_or_save_report(
                    ReportsMenu.SHOW_SALES
                )
            elif choice == '4':
                date = datetime.strptime(input(
                    "Enter date in format (YYYY-MM-DD): "),
                    "%Y-%m-%d"
                )
                validated_date = DateValidator.validate_date(date)
                if validated_date:
                    self.report_processor.display_or_save_report(
                        ReportsMenu.SHOW_REPORTS_BY_DATE, date=date
                    )
            elif choice == '5':
                start_date = datetime.strptime(input(
                    "Enter start date in format (YYYY-MM-DD): "),
                    "%Y-%m-%d"
                )
                validated_start_date = DateValidator.validate_date(start_date)
                end_date = datetime.strptime(input(
                    "Enter end date in format (YYYY-MM-DD): "),
                    "%Y-%m-%d"
                )
                validated_end_date = DateValidator.validate_date(end_date)
                if validated_start_date and validated_end_date:
                    self.report_processor.display_or_save_report(
                        ReportsMenu.SHOW_SALES_IN_PERIOD,
                        start_date=start_date, end_date=end_date
                    )
            elif choice == '6':
                employee_id = input("Enter employee ID "
                                    "(ID must be an integer): >> ")
                self.report_processor.display_or_save_report(
                    ReportsMenu.SHOW_SALES_BY_EMPLOYEE,
                    employee_id=employee_id
                )
            elif choice == '7':
                start_date = datetime.strptime(input(
                    "Enter start date in format (YYYY-MM-DD): "),
                    "%Y-%m-%d"
                )
                validated_start_date = DateValidator.validate_date(start_date)
                end_date = datetime.strptime(input(
                    "Enter end date in format (YYYY-MM-DD): "),
                    "%Y-%m-%d"
                )
                validated_end_date = DateValidator.validate_date(end_date)
                if validated_start_date and validated_end_date:
                    self.report_processor.display_or_save_report(
                        ReportsMenu.SHOW_MOST_SALE_CAR_IN_PERIOD,
                        start_date=start_date, end_date=end_date
                )
            elif choice == '8':
                start_date = datetime.strptime(input(
                    "Enter start date in format (YYYY-MM-DD): "),
                    "%Y-%m-%d"
                )
                validated_start_date = DateValidator.validate_date(start_date)
                end_date = datetime.strptime(input(
                    "Enter end date in format (YYYY-MM-DD): "),
                    "%Y-%m-%d"
                )
                validated_end_date = DateValidator.validate_date(end_date)
                if validated_start_date and validated_end_date:
                    self.report_processor.display_or_save_report(
                        ReportsMenu.SHOW_TOP_EMPLOYEE_IN_PERIOD,
                        start_date=start_date, end_date=end_date
                )
            elif choice == '9':
                start_date = datetime.strptime(input(
                    "Enter start date in format (YYYY-MM-DD): "),
                    "%Y-%m-%d"
                )
                validated_start_date = DateValidator.validate_date(start_date)
                end_date = datetime.strptime(input(
                    "Enter end date in format (YYYY-MM-DD): "),
                    "%Y-%m-%d"
                )
                validated_end_date = DateValidator.validate_date(end_date)
                if validated_start_date and validated_end_date:
                    self.report_processor.display_or_save_report(
                        ReportsMenu.SHOW_PROFIT_IN_PERIOD,
                        start_date=start_date, end_date=end_date
                )
            elif choice == '10':
                break
            else:
                print("Invalid choice, please try again.")



    def save_data(self):
        filename = input(
            "Enter filename to save data: >> "
        )
        self.salon.save_data(filename)

    def load_data(self):
        filename = input(
            "Enter filename to load data: >> "
        )
        self.salon.load_data(filename)


if __name__ == "__main__":
    salon = AutoSalon()
    menu = AutoSalonMenu(salon)
    menu.start()

