from classes.data_manager import DataManager

class Team:
    last_id = 0
    available_ids = []

    def __init__(self, team_id, name, genre, categorie):
        self.team_id = team_id
        self.name = name
        self.genre = genre
        self.categorie = categorie

        if team_id > Team.last_id:
            Team.last_id = team_id

    @classmethod
    def create_new(cls, name, genre, categorie):
        if cls.available_ids:
            new_id = cls.available_ids.pop(0)
        else:
            cls.last_id += 1
            new_id = cls.last_id
        return cls(new_id, name, genre, categorie)

    @staticmethod
    def delete(team):
        Team.available_ids.append(team.team_id)

    def update_details(self, name, genre, categorie):
        self.name = name
        self.genre = genre
        self.categorie = categorie

    def to_dict(self):
        return {
            'team_id': self.team_id,
            'name': self.name,
            'genre': self.genre,
            'categorie': self.categorie
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data['team_id'], data['name'], data['genre'], data['categorie']
        )

    @staticmethod
    def save_to_file(teams):
        DataManager.save_to_file([team.to_dict() for team in teams], 'data/teams.json')

    @staticmethod
    def load_from_file():
        teams_data = DataManager.load_from_file('data/teams.json')
        if teams_data is None:
            teams_data = []
        teams = [Team.from_dict(data) for data in teams_data]

        if teams:
            Team.last_id = max(team.team_id for team in teams)

        return teams
