from classes.person import Person
from classes.data_manager import DataManager

class Player(Person):
    last_id = 0
    available_ids = []

    def __init__(self, person_ID, last_name, first_name, birth_date, salary, contract, address, phone_number, position, jersey_number):
        super().__init__(int(person_ID), last_name, first_name, birth_date, salary, contract, address, phone_number)
        self.position = position
        self.jersey_number = jersey_number

        # Mettre à jour le dernier ID utilisé
        person_ID = int(person_ID)
        if person_ID > Player.last_id:
            Player.last_id = person_ID

    @classmethod
    def create_new(cls, last_name, first_name, birth_date, salary, contract, address, phone_number, position, jersey_number):
        if cls.available_ids:
            new_id = cls.available_ids.pop(0)  # Réutiliser un ID disponible
        else:
            cls.last_id += 1
            new_id = cls.last_id
        return cls(new_id, last_name, first_name, birth_date, salary, contract, address, phone_number, position, jersey_number)

    @staticmethod
    def delete(player):
        Player.available_ids.append(player.person_ID)

    def update_details(self, person_ID, last_name, first_name, birth_date, salary, contract, address, phone_number, position, jersey_number):
        """Met à jour les détails du joueur."""
        self.person_ID = int(person_ID)
        self.last_name = last_name
        self.first_name = first_name
        self.birth_date = birth_date
        self.salary = salary
        self.contract = contract
        self.address = address
        self.phone_number = phone_number
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
            int(data['person_ID']), data['last_name'], data['first_name'],
            data['birth_date'], data['salary'], data['contract'],
            data['address'], data['phone_number'], data['position'],
            data['jersey_number']
        )

    @staticmethod
    def save_to_file(players):
        DataManager.save_to_file([player.to_dict() for player in players], 'data/players.json')

    @staticmethod
    def load_from_file():
        players_data = DataManager.load_from_file('data/players.json')
        players = [Player.from_dict(data) for data in players_data]
        
        # Mettre à jour le compteur d'ID pour correspondre au plus grand ID existant
        if players:
            Player.last_id = max(player.person_ID for player in players)
        
        return players
