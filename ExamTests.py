from datetime import datetime
from Exam import (Employee, Car, AutoSalon, ReportGenerator,
                  ReportsMenu, Sale, SaveDataToFile,
                  LoadDataFromFile, DateValidator)
import pytest


@pytest.fixture
def employee():
    return Employee(1, "John Connor", "Seller",
                    "123456789", "judgmentday@gmail.com")


@pytest.fixture
def car():
    return Car(1, "Ford", "Mustang", 2024,
               5000, 10000)


@pytest.fixture
def sale(employee, car):
    return Sale(employee, car, datetime(2024, 8, 1), 7000)


@pytest.fixture
def autosalon(employee, car):
    autosalon = AutoSalon()
    autosalon.add_employee(employee)
    autosalon.add_car(car)
    return autosalon


def test_create_employee(employee):
    assert employee.employee_id == 1
    assert employee.full_name == "John Connor"
    assert employee.position == "Seller"
    assert employee.phone_number == "123456789"
    assert employee.email == "judgmentday@gmail.com"


def test_employee_repr(employee):
    assert repr(employee) == ("Employee: ID - 1, Full name - John Connor, "
                              "Position - Seller, Phone number - 123456789, "
                              "Email - judgmentday@gmail.com")


def test_create_car(car):
    assert car.car_id == 1
    assert car.producer == "Ford"
    assert car.model == "Mustang"
    assert car.release_year == 2024
    assert car.cost == 5000
    assert car.potential_sale_price == 10000


def test_car_repr(car):
    assert repr(car) == ("Car: ID - 1, Producer - Ford, Model - Mustang, "
                         "Release year - 2024, Cost - 5000, "
                         "Potential sale price - 10000")


def test_create_sale(sale, employee, car):
    assert sale.employee == employee
    assert sale.car == car
    assert sale.sale_date == datetime(2024, 8, 1)
    assert sale.real_sale_price == 7000


def test_sale_repr(sale):
    assert repr(sale) == ("Sale: Employee - 1, Car - Car: ID - 1, Producer - Ford, "
                          "Model - Mustang, Release year - 2024, Cost - 5000, "
                          "Potential sale price - 10000, "
                          "Sale date - 2024-08-01 00:00:00, "
                          "Real sale price - 7000")


def test_add_employee(autosalon, employee):
    assert autosalon.employees[employee.employee_id] == employee


def test_remove_employee(autosalon, employee):
    autosalon.remove_employee(employee)
    assert employee.employee_id not in autosalon.employees


def test_add_car(autosalon, car):
    assert autosalon.cars[car.car_id] == car


def test_remove_car(autosalon, car):
    autosalon.remove_car(car)
    assert car.car_id not in autosalon.cars


def test_register_sale(autosalon, employee, car):
    autosalon.register_sale(employee.employee_id, car.car_id,
                            datetime(2024, 8, 1), 7000)
    assert len(autosalon.sales) == 1
    assert car.car_id not in autosalon.cars


def test_show_employees_report(autosalon):
    report_generator = ReportGenerator(autosalon)
    employees_report = report_generator.generate_report(ReportsMenu.SHOW_EMPLOYEES)
    assert len(employees_report) == 1


def test_show_cars_report(autosalon):
    report_generator = ReportGenerator(autosalon)
    cars_report = report_generator.generate_report(ReportsMenu.SHOW_CARS)
    assert len(cars_report) == 1


def test_show_sales_report(autosalon, sale):
    autosalon.sales.append(sale)
    report_generator = ReportGenerator(autosalon)
    sales_report = report_generator.generate_report(ReportsMenu.SHOW_SALES)
    assert len(sales_report) == 1


def test_validate_date():
    future_date = datetime(2025, 1, 1)
    assert DateValidator.validate_date(future_date) is None

    valid_date = datetime(2023, 1, 1)
    assert DateValidator.validate_date(valid_date) == valid_date



































