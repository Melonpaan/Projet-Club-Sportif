# src/model/team.py
from src.controller.data_manager import DataManager


class Team:
    def __init__(self, team_id, name, data_dir):
        self.team_id = team_id
        self.name = name
        self.data_manager = DataManager(data_dir)
        self.players = []
        self.staff = []
        self.load_team_data()

    def load_team_data(self):
        teams = self.data_manager.load_teams()
        team_data = next((team for team in teams if team['team_id'] == self.team_id), None)
        if team_data:
            self.players = team_data.get('players', [])
            self.staff = team_data.get('staff', [])

    def save_team_data(self):
        teams = self.data_manager.load_teams()
        team_data = {
            'team_id': self.team_id,
            'name': self.name,
            'players': self.players,
            'staff': self.staff
        }
        existing_team_index = next((index for index, team in enumerate(teams) if team['team_id'] == self.team_id), None)
        if existing_team_index is not None:
            teams[existing_team_index] = team_data
        else:
            teams.append(team_data)
        self.data_manager.save_teams(teams)

    def add_player(self, player):
        self.players.append(player)
        self.save_team_data()

    def remove_player(self, player_id):
        self.players = [p for p in self.players if p.person_id != player_id]
        self.save_team_data()

    def add_staff(self, staff):
        self.staff.append(staff)
        self.save_team_data()

    def remove_staff(self, staff_id):
        self.staff = [s for s in self.staff if s.person_id != staff_id]
        self.save_team_data()

    def __str__(self):
        return f"Team: {self.name} (ID: {self.team_id})"
