# src/gui/player_dialogs.py
import tkinter as tk
from tkinter import simpledialog, messagebox
from datetime import date


class AddPlayerDialog(simpledialog.Dialog):
    def __init__(self, parent, data_manager, callback):
        self.data_manager = data_manager
        self.callback = callback
        super().__init__(parent, "Ajouter Joueur")

    def body(self, master):
        tk.Label(master, text="ID").grid(row=0)
        tk.Label(master, text="Nom").grid(row=1)
        tk.Label(master, text="Prénom").grid(row=2)
        tk.Label(master, text="Date de Naissance (YYYY-MM-DD)").grid(row=3)
        tk.Label(master, text="Poste").grid(row=4)
        tk.Label(master, text="Salaire").grid(row=5)

        self.entry_id = tk.Entry(master)
        self.entry_last_name = tk.Entry(master)
        self.entry_first_name = tk.Entry(master)
        self.entry_birth_date = tk.Entry(master)
        self.entry_position = tk.Entry(master)
        self.entry_salary = tk.Entry(master)

        self.entry_id.grid(row=0, column=1)
        self.entry_last_name.grid(row=1, column=1)
        self.entry_first_name.grid(row=2, column=1)
        self.entry_birth_date.grid(row=3, column=1)
        self.entry_position.grid(row=4, column=1)
        self.entry_salary.grid(row=5, column=1)

        return self.entry_id  # initial focus

    def validate(self):
        try:
            self.player_id = int(self.entry_id.get())
            self.last_name = self.entry_last_name.get()
            self.first_name = self.entry_first_name.get()
            self.birth_date = date.fromisoformat(self.entry_birth_date.get())
            self.position = self.entry_position.get()
            self.salary = float(self.entry_salary.get())
            return True
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer des informations valides.")
            return False

    def apply(self):
        player = {
            "person_id": self.player_id,
            "last_name": self.last_name,
            "first_name": self.first_name,
            "birth_date": self.birth_date.isoformat(),
            "position": self.position,
            "salary": self.salary,
            "age": self.calculate_age(self.birth_date)
        }
        players = self.data_manager.load_players()
        players.append(player)
        self.data_manager.save_players(players)
        self.callback()

    def calculate_age(self, birth_date):
        today = date.today()
        return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))


class EditPlayerDialog(simpledialog.Dialog):
    def __init__(self, parent, data_manager, player_id, callback):
        self.data_manager = data_manager
        self.player_id = player_id
        self.callback = callback
        super().__init__(parent, "Modifier Joueur")

    def body(self, master):
        player = self.get_player_by_id(self.player_id)
        if not player:
            messagebox.showerror("Erreur", "Joueur non trouvé.")
            self.destroy()
            return

        tk.Label(master, text="ID").grid(row=0)
        tk.Label(master, text="Nom").grid(row=1)
        tk.Label(master, text="Prénom").grid(row=2)
        tk.Label(master, text="Date de Naissance (YYYY-MM-DD)").grid(row=3)
        tk.Label(master, text="Poste").grid(row=4)
        tk.Label(master, text="Salaire").grid(row=5)

        self.entry_id = tk.Entry(master)
        self.entry_last_name = tk.Entry(master)
        self.entry_first_name = tk.Entry(master)
        self.entry_birth_date = tk.Entry(master)
        self.entry_position = tk.Entry(master)
        self.entry_salary = tk.Entry(master)

        self.entry_id.insert(0, player['person_id'])
        self.entry_id.config(state='disabled')  # ID should not be editable
        self.entry_last_name.insert(0, player['last_name'])
        self.entry_first_name.insert(0, player['first_name'])
        self.entry_birth_date.insert(0, player['birth_date'])
        self.entry_position.insert(0, player['position'])
        self.entry_salary.insert(0, player['salary'])

        self.entry_id.grid(row=0, column=1)
        self.entry_last_name.grid(row=1, column=1)
        self.entry_first_name.grid(row=2, column=1)
        self.entry_birth_date.grid(row=3, column=1)
        self.entry_position.grid(row=4, column=1)
        self.entry_salary.grid(row=5, column=1)

        return self.entry_last_name  # initial focus

    def validate(self):
        try:
            self.new_last_name = self.entry_last_name.get()
            self.new_first_name = self.entry_first_name.get()
            self.new_birth_date = date.fromisoformat(self.entry_birth_date.get())
            self.new_position = self.entry_position.get()
            self.new_salary = float(self.entry_salary.get())
            return True
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer des informations valides.")
            return False

    def apply(self):
        players = self.data_manager.load_players()
        for player in players:
            if player['person_id'] == self.player_id:
                player['last_name'] = self.new_last_name
                player['first_name'] = self.new_first_name
                player['birth_date'] = self.new_birth_date.isoformat()
                player['position'] = self.new_position
                player['salary'] = self.new_salary
                player['age'] = self.calculate_age(self.new_birth_date)
                break

        self.data_manager.save_players(players)
        self.callback()

    def get_player_by_id(self, player_id):
        players = self.data_manager.load_players()
        for player in players:
            if player['person_id'] == player_id:
                return player
        return None

    def calculate_age(self, birth_date):
        today = date.today()
        return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
