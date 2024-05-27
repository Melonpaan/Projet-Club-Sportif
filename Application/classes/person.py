class Person:
    def __init__(self, person_ID, last_name, first_name, birth_date, salary, contract, address, phone_number):
        self.person_ID = person_ID
        self.last_name = last_name
        self.first_name = first_name
        self.birth_date = birth_date
        self.salary = salary
        self.contract = contract
        self.address = address
        self.phone_number = phone_number

    def __str__(self):
        return f"Person[ID={self.person_ID}, Name={self.first_name} {self.last_name}, Birth Date={self.birth_date}, Salary={self.salary}, Contract={self.contract}, Address={self.address}, Phone Number={self.phone_number}]"
    
    def __repr__(self):
        return self.__str__()
    
    def to_dict(self):
        return {
            'person_ID': self.person_ID,
            'last_name': self.last_name,
            'first_name': self.first_name,
            'birth_date': self.birth_date,
            'salary': self.salary,
            'contract': self.contract,
            'address': self.address,
            'phone_number': self.phone_number
        }
