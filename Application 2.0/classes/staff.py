from classes.person import Person
from classes.contract import Contract
from classes.data_manager import DataManager

class Staff(Person):
    last_id = 0
    available_ids = []

    def __init__(self, person_ID, last_name, first_name, birth_date, contract, address, phone_number, role):
        super().__init__(int(person_ID), last_name, first_name, birth_date, contract, address, phone_number)
        self.role = role

        person_ID = int(person_ID)
        if person_ID > Staff.last_id:
            Staff.last_id = person_ID

    @classmethod
    def create_new(cls, last_name, first_name, birth_date, contract, address, phone_number, role):
        if cls.available_ids:
            new_id = cls.available_ids.pop(0)
        else:
            cls.last_id += 1
            new_id = cls.last_id
        return cls(new_id, last_name, first_name, birth_date, contract, address, phone_number, role)

    @staticmethod
    def delete(staff):
        Staff.available_ids.append(staff.person_ID)

    def update_details(self, last_name, first_name, birth_date, contract, address, phone_number, role):
        self.last_name = last_name
        self.first_name = first_name
        self.birth_date = birth_date
        self.contract.update(contract.start_date, contract.end_date, contract.salary)
        self.address = address
        self.phone_number = phone_number
        self.role = role

    def to_dict(self):
        data = super().to_dict()
        data.update({
            'role': self.role
        })
        return data

    @classmethod
    def from_dict(cls, data):
        contract = Contract.from_dict(data['contract'])
        return cls(
            int(data['person_ID']), data['last_name'], data['first_name'],
            data['birth_date'], contract, data['address'], data['phone_number'],
            data['role']
        )

    @staticmethod
    def save_to_file(staff_members):
        DataManager.save_to_file([staff.to_dict() for staff in staff_members], 'data/staff.json')

    @staticmethod
    def load_from_file():
        staff_data = DataManager.load_from_file('data/staff.json')
        staff_members = [Staff.from_dict(data) for data in staff_data]
        
        if staff_members:
            Staff.last_id = max(staff.person_ID for staff in staff_members)
        
        return staff_members
