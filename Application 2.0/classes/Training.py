from classes.data_manager import DataManager

class Training:
    def __init__(self, date, my_team, location, players=None):
        self.date = date
        self.my_team = my_team
        self.location = location
        self.players = players if players else []

    def add_training(self, training_data, filename='data/trainings.json'):
        trainings = DataManager.load_from_file(filename) or []
        trainings.append(training_data)
        DataManager.save_to_file(trainings, filename)

    def add_team_to_training(self, team_data, filename='data/players.json'):
        teams = DataManager.load_from_file(filename)
        if teams is not None:
            teams.append(team_data)
            DataManager.save_to_file(teams, filename)
        else:
            raise FileNotFoundError(f"The file {filename} does not exist.")

