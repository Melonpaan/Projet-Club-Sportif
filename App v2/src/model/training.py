# src/model/training.py
from src.controller.data_manager import DataManager


class Training:
    def __init__(self, training_id, team, date, stadium, data_dir):
        self.training_id = training_id
        self.team = team
        self.date = date
        self.stadium = stadium
        self.data_manager = DataManager(data_dir)
        self.load_training_data()

    def load_training_data(self):
        trainings = self.data_manager.load_trainings()
        training_data = next((training for training in trainings if training['training_id'] == self.training_id), None)
        if training_data:
            self.team = training_data['team']
            self.date = training_data['date']
            self.stadium = training_data['stadium']

    def save_training_data(self):
        trainings = self.data_manager.load_trainings()
        training_data = {
            'training_id': self.training_id,
            'team': self.team,
            'date': self.date,
            'stadium': self.stadium
        }
        existing_training_index = next(
            (index for index, training in enumerate(trainings) if training['training_id'] == self.training_id), None)
        if existing_training_index is not None:
            trainings[existing_training_index] = training_data
        else:
            trainings.append(training_data)
        self.data_manager.save_trainings(trainings)

    def __str__(self):
        return f"Training: {self.team} on {self.date} at {self.stadium}"
