# src/model/club.py
from player import Player
from staff import Staff
from src.controller.data_manager import DataManager


class Club:
    def __init__(self, name, data_dir):
        self.name = name
        self.data_manager = DataManager(data_dir)
        self.players = self.data_manager.load_players()
        self.staff = self.data_manager.load_staff()

    def add_player(self, player):
        self.players.append(player)
        self.data_manager.save_players(self.players)

    def remove_player(self, player_id):
        self.players = [p for p in self.players if p.person_id != player_id]
        self.data_manager.save_players(self.players)

    def add_staff(self, staff):
        self.staff.append(staff)
        self.data_manager.save_staff(self.staff)

    def remove_staff(self, staff_id):
        self.staff = [s for s in self.staff if s.person_id != staff_id]
        self.data_manager.save_staff(self.staff)

    def get_total_salary(self):
        total_salary = sum(p.salary for p in self.players) + sum(s.salary for s in self.staff)
        return total_salary
