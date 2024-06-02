import json
import os

class Club:
    def __init__(self, name, address, president):
        self.name = name
        self.address = address
        self.president = president
        self.teams = []

    def to_dict(self):
        return {
            'name': self.name,
            'address': self.address,
            'president': self.president,
            'teams': self.teams
        }

    @classmethod
    def from_dict(cls, data):
        club = cls(data['name'], data['address'], data['president'])
        club.teams = data.get('teams', [])
        return club

    def save_to_file(self, filename='data/club.json'):
        folder = os.path.dirname(filename)
        if not os.path.exists(folder):
            os.makedirs(folder)
        with open(filename, 'w') as f:
            json.dump(self.to_dict(), f, indent=4)

    @classmethod
    def load_from_file(cls, filename='data/club.json'):
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                data = json.load(f)
                return cls.from_dict(data)
        return cls("Nom du Club", "Adresse du Club", "Président du Club")

    def add_team(self, team_name):
        if team_name not in self.teams:  # Ajouter une vérification pour éviter les doublons
            self.teams.append(team_name)
            self.save_to_file()  # Sauvegarder après l'ajout

    def remove_team(self, team_name):
        if team_name in self.teams:  # Vérifier si l'équipe existe avant de la supprimer
            self.teams.remove(team_name)
            self.save_to_file()  # Sauvegarder après la suppression

