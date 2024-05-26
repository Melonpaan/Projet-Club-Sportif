# src/model/match.py
from src.controller.data_manager import DataManager


class Match:
    def __init__(self, match_id, team_home, team_away, date, stadium, data_dir):
        self.match_id = match_id
        self.team_home = team_home
        self.team_away = team_away
        self.date = date
        self.stadium = stadium
        self.data_manager = DataManager(data_dir)
        self.load_match_data()

    def load_match_data(self):
        matches = self.data_manager.load_matches()
        match_data = next((match for match in matches if match['match_id'] == self.match_id), None)
        if match_data:
            self.team_home = match_data['team_home']
            self.team_away = match_data['team_away']
            self.date = match_data['date']
            self.stadium = match_data['stadium']

    def save_match_data(self):
        matches = self.data_manager.load_matches()
        match_data = {
            'match_id': self.match_id,
            'team_home': self.team_home,
            'team_away': self.team_away,
            'date': self.date,
            'stadium': self.stadium
        }
        existing_match_index = next(
            (index for index, match in enumerate(matches) if match['match_id'] == self.match_id), None)
        if existing_match_index is not None:
            matches[existing_match_index] = match_data
        else:
            matches.append(match_data)
        self.data_manager.save_matches(matches)

    def __str__(self):
        return f"Match: {self.team_home} vs {self.team_away} on {self.date} at {self.stadium}"
