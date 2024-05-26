# src/model/player.py
from person import Person


class Player(Person):
    def __init__(self, person_id, first_name, last_name, birth_date, salary, position, goals_scored=0, assists=0,
                 address=None, phone_number=None, email=None):
        super().__init__(person_id, first_name, last_name, birth_date, salary, address, phone_number, email)
        self.position = position
        self.goals_scored = goals_scored
        self.assists = assists

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def update_position(self, new_position):
        self.position = new_position

    def __str__(self):
        return (super().__str__() +
                f", Position: {self.position}, Goals Scored: {self.goals_scored}, Assists: {self.assists}")
