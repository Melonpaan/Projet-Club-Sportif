from classes.person import Person
from classes.contract import Contract
from classes.data_manager import DataManager

class Player(Person):
    last_id = 0
    available_ids = []

    def __init__(self, person_ID, last_name, first_name, birth_date, contract, address, phone_number, position, jersey_number,gender):
        super().__init__(int(person_ID), last_name, first_name, birth_date, contract, address, phone_number, gender)
        self.position = position
        self.jersey_number = jersey_number

        person_ID = int(person_ID)
        if person_ID > Player.last_id:
            Player.last_id = person_ID

    @classmethod
    def create_new(cls, last_name, first_name, birth_date, contract, address, phone_number, position, jersey_number, gender):
        if cls.available_ids:
            new_id = cls.available_ids.pop(0)
        else:
            cls.last_id += 1
            new_id = cls.last_id
        return cls(new_id, last_name, first_name, birth_date, contract, address, phone_number, position, jersey_number,gender)

    @staticmethod
    def delete(player):
        Player.available_ids.append(player.person_ID)

    def update_details(self, last_name, first_name, birth_date, contract, address, phone_number, position, jersey_number,gender):
        self.last_name = last_name
        self.first_name = first_name
        self.birth_date = birth_date
        self.contract.update(contract.start_date, contract.end_date, contract.salary)
        self.address = address
        self.phone_number = phone_number
        self.position = position
        self.jersey_number = jersey_number
        self.gender = gender 

    def to_dict(self):
        data = super().to_dict()
        data.update({
            'position': self.position,
            'jersey_number': self.jersey_number
        })
        return data

    @classmethod
    def from_dict(cls, data):
        contract = Contract.from_dict(data['contract'])
        return cls(
            int(data['person_ID']), data['last_name'], data['first_name'],
            data['birth_date'], contract, data['address'], data['phone_number'],
            data['position'], data['jersey_number'], data['gender']
        )

    @staticmethod
    def save_to_file(players):
        DataManager.save_to_file([player.to_dict() for player in players], 'data/players.json')

    @staticmethod
    def load_from_file():
        players_data = DataManager.load_from_file('data/players.json')
        players = [Player.from_dict(data) for data in players_data]
        
        if players:
            Player.last_id = max(player.person_ID for player in players)
        
        return players
