from classes.contract import Contract

class Person:
    def __init__(self, person_ID, last_name, first_name, birth_date, contract, address, phone_number):
        self.person_ID = person_ID
        self.last_name = last_name
        self.first_name = first_name
        self.birth_date = birth_date
        self.contract = contract  # Attribut contract
        self.address = address
        self.phone_number = phone_number

    def to_dict(self):
        return {
            'person_ID': self.person_ID,
            'last_name': self.last_name,
            'first_name': self.first_name,
            'birth_date': self.birth_date,
            'contract': self.contract.to_dict(),  # Convertir le contrat en dict
            'address': self.address,
            'phone_number': self.phone_number 
        }

    @classmethod
    def from_dict(cls, data):
        contract = Contract.from_dict(data['contract'])  # Recréer l'objet Contract
        return cls(
            data['person_ID'],
            data['last_name'],
            data['first_name'],
            data['birth_date'],
            contract,  # Passer l'objet Contract
            data['address'],
            data['phone_number']
        )
