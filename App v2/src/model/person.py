# src/model/person.py
from abc import ABC, abstractmethod
from datetime import date


class Person(ABC):
    def __init__(self, person_id, first_name, last_name, birth_date, salary, address=None, phone_number=None,
                 email=None):
        self.person_id = person_id
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.salary = salary
        self.address = address
        self.phone_number = phone_number
        self.email = email

    @abstractmethod
    def get_full_name(self):
        pass

    def get_age(self):
        today = date.today()
        age = today.year - self.birth_date.year - (
                    (today.month, today.day) < (self.birth_date.month, self.birth_date.day))
        return age

    def update_address(self, new_address):
        self.address = new_address

    def update_phone_number(self, new_phone_number):
        self.phone_number = new_phone_number

    def update_email(self, new_email):
        self.email = new_email

    def update_salary(self, new_salary):
        self.salary = new_salary

    def __str__(self):
        return (f"{self.get_full_name()} (ID: {self.person_id}, Age: {self.get_age()}, "
                f"Address: {self.address}, Phone: {self.phone_number}, Email: {self.email}, Salary: {self.salary})")
