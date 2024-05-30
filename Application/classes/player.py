from classes.person import Person
from classes.data_manager import DataManager

class Player(Person):
    def __init__(self, person_ID, last_name, first_name, birth_date, salary, contract, address, phone_number, position, jersey_number):
        super().__init__(person_ID, last_name, first_name, birth_date, salary, contract, address, phone_number)
        self.position = position
        self.jersey_number = jersey_number

    def to_dict(self):
        data = super().to_dict()
        data.update({
            'position': self.position,
            'jersey_number': self.jersey_number
        })
        return data

    @classmethod
    def from_dict(cls, data):
        return cls(
            data['person_ID'], data['last_name'], data['first_name'],
            data['birth_date'], data['salary'], data['contract'],
            data['address'], data['phone_number'], data['position'],
            data['jersey_number']
        )

    @staticmethod
    def save_to_file(joueurs):
        DataManager.save_to_file([joueur.to_dict() for joueur in joueurs], 'data/joueurs.json')

    @staticmethod
    def load_from_file():
        joueurs_data = DataManager.load_from_file('data/joueurs.json')
        return [Player.from_dict(data) for data in joueurs_data]