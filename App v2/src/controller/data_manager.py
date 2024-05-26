# src/controller/data_manager.py
import json
import os


class DataManager:
    def __init__(self, data_dir):
        self.data_dir = data_dir
        self._ensure_data_directory_exists()

    def _ensure_data_directory_exists(self):
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
        self._ensure_file_exists('players.json')
        self._ensure_file_exists('staff.json')
        self._ensure_file_exists('teams.json')
        self._ensure_file_exists('matches.json')
        self._ensure_file_exists('trainings.json')
        self._ensure_file_exists('transfers.json')
        self._ensure_file_exists('seasons.json')
        self._ensure_file_exists('statistics.json')
        self._ensure_file_exists('sanctions.json')
        self._ensure_file_exists('stadiums.json')

    def _ensure_file_exists(self, filename):
        file_path = self._get_file_path(filename)
        if not os.path.exists(file_path):
            with open(file_path, 'w') as file:
                json.dump([], file)

    def _get_file_path(self, filename):
        return os.path.join(self.data_dir, filename)

    def load_data(self, filename):
        file_path = self._get_file_path(filename)
        if not os.path.exists(file_path):
            return []
        with open(file_path, 'r') as file:
            return json.load(file)

    def save_data(self, filename, data):
        file_path = self._get_file_path(filename)
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)

    def load_players(self):
        return self.load_data('players.json')

    def save_players(self, players):
        self.save_data('players.json', players)

    def load_staff(self):
        return self.load_data('staff.json')

    def save_staff(self, staff):
        self.save_data('staff.json', staff)

    def load_teams(self):
        teams = self.load_data('teams.json')
        for team in teams:
            team.setdefault('players', [])
            team.setdefault('staff', [])
        return teams

    def save_teams(self, teams):
        self.save_data('teams.json', teams)

    # Ajouter les méthodes de chargement et de sauvegarde pour les autres entités...

    def load_matches(self):
        return self.load_data('matches.json')

    def save_matches(self, matches):
        self.save_data('matches.json', matches)

    def load_trainings(self):
        return self.load_data('trainings.json')

    def save_trainings(self, trainings):
        self.save_data('trainings.json', trainings)

    def load_transfers(self):
        return self.load_data('transfers.json')

    def save_transfers(self, transfers):
        self.save_data('transfers.json', transfers)

    def load_seasons(self):
        return self.load_data('seasons.json')

    def save_seasons(self, seasons):
        self.save_data('seasons.json', seasons)

    def load_statistics(self):
        return self.load_data('statistics.json')

    def save_statistics(self, statistics):
        self.save_data('statistics.json', statistics)

    def load_sanctions(self):
        return self.load_data('sanctions.json')

    def save_sanctions(self, sanctions):
        self.save_data('sanctions.json', sanctions)

    def load_stadiums(self):
        return self.load_data('stadiums.json')

    def save_stadiums(self, stadiums):
        self.save_data('stadiums.json', stadiums)
