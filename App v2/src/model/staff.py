# src/model/staff.py
from person import Person


class Staff(Person):
    def __init__(self, person_id, first_name, last_name, birth_date, salary, role, address=None, phone_number=None,
                 email=None):
        super().__init__(person_id, first_name, last_name, birth_date, salary, address, phone_number, email)
        self.role = role

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def update_role(self, new_role):
        self.role = new_role

    def __str__(self):
        return super().__str__() + f", Role: {self.role}"

