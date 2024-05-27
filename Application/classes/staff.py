from classes.person import Person
from classes.data_manager import DataManager

class Staff(Person):
    def __init__(self, person_ID, last_name, first_name, birth_date, salary, contract, address, phone_number, role):
        super().__init__(person_ID, last_name, first_name, birth_date, salary, contract, address, phone_number)
        self.role = role
    @staticmethod
    def add_staff(gui_manager):
        pass
    @staticmethod
    def modify_staff(gui_manager):
        pass
    @staticmethod
    def delete_staff(gui_manager):
        pass