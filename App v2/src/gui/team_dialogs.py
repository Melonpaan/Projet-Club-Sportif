# src/gui/team_dialogs.py
import tkinter as tk
from tkinter import simpledialog, messagebox

class AddTeamDialog(simpledialog.Dialog):
    def __init__(self, parent, data_manager, callback):
        self.data_manager = data_manager
        self.callback = callback
        super().__init__(parent, "Ajouter Équipe")

    def body(self, master):
        tk.Label(master, text="ID").grid(row=0)
        tk.Label(master, text="Nom de l'équipe").grid(row=1)

        self.entry_id = tk.Entry(master)
        self.entry_team_name = tk.Entry(master)

        self.entry_id.grid(row=0, column=1)
        self.entry_team_name.grid(row=1, column=1)

        return self.entry_id  # initial focus

    def validate(self):
        try:
            self.team_id = int(self.entry_id.get())
            self.team_name = self.entry_team_name.get()
            return True
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer des informations valides.")
            return False

    def apply(self):
        team = {
            "team_id": self.team_id,
            "team_name": self.team_name,
            "players": [],
            "staff": []
        }
        teams = self.data_manager.load_teams()
        teams.append(team)
        self.data_manager.save_teams(teams)
        self.callback()

class EditTeamDialog(simpledialog.Dialog):
    def __init__(self, parent, data_manager, team_id, callback):
        self.data_manager = data_manager
        self.team_id = team_id
        self.callback = callback
        super().__init__(parent, "Modifier Équipe")

    def body(self, master):
        team = self.get_team_by_id(self.team_id)
        if not team:
            messagebox.showerror("Erreur", "Équipe non trouvée.")
            self.destroy()
            return

        tk.Label(master, text="ID").grid(row=0)
        tk.Label(master, text="Nom de l'équipe").grid(row=1)
        tk.Label(master, text="Joueurs disponibles").grid(row=2)
        tk.Label(master, text="Staff disponible").grid(row=3)
        tk.Label(master, text="Joueurs de l'équipe").grid(row=4)
        tk.Label(master, text="Staff de l'équipe").grid(row=5)

        self.entry_id = tk.Entry(master)
        self.entry_team_name = tk.Entry(master)
        self.listbox_available_players = tk.Listbox(master, selectmode=tk.MULTIPLE)
        self.listbox_available_staff = tk.Listbox(master, selectmode=tk.MULTIPLE)
        self.listbox_team_players = tk.Listbox(master, selectmode=tk.MULTIPLE)
        self.listbox_team_staff = tk.Listbox(master, selectmode=tk.MULTIPLE)

        self.entry_id.insert(0, team['team_id'])
        self.entry_id.config(state='disabled')  # ID should not be editable
        self.entry_team_name.insert(0, team['team_name'])

        self.entry_id.grid(row=0, column=1)
        self.entry_team_name.grid(row=1, column=1)
        self.listbox_available_players.grid(row=2, column=1)
        self.listbox_available_staff.grid(row=3, column=1)
        self.listbox_team_players.grid(row=4, column=1)
        self.listbox_team_staff.grid(row=5, column=1)

        # Ajouter les boutons Ajouter et Retirer pour les joueurs
        self.add_player_button = tk.Button(master, text="Ajouter Joueur", command=self.add_player_to_team)
        self.remove_player_button = tk.Button(master, text="Retirer Joueur", command=self.remove_player_from_team)
        self.add_player_button.grid(row=2, column=2, padx=5, pady=5)
        self.remove_player_button.grid(row=4, column=2, padx=5, pady=5)

        # Ajouter les boutons Ajouter et Retirer pour le staff
        self.add_staff_button = tk.Button(master, text="Ajouter Staff", command=self.add_staff_to_team)
        self.remove_staff_button = tk.Button(master, text="Retirer Staff", command=self.remove_staff_from_team)
        self.add_staff_button.grid(row=3, column=2, padx=5, pady=5)
        self.remove_staff_button.grid(row=5, column=2, padx=5, pady=5)

        # Populate listboxes with players and staff
        available_players = [player for player in self.data_manager.load_players() if player['person_id'] not in team['players']]
        for player in available_players:
            self.listbox_available_players.insert(tk.END, f"{player['person_id']} - {player['last_name']} {player['first_name']}")

        available_staff = [staff for staff in self.data_manager.load_staff() if staff['person_id'] not in team['staff']]
        for staff in available_staff:
            self.listbox_available_staff.insert(tk.END, f"{staff['person_id']} - {staff['last_name']} {staff['first_name']}")

        for player_id in team['players']:
            player = self.get_person_by_id(player_id, self.data_manager.load_players())
            if player:
                self.listbox_team_players.insert(tk.END, f"{player['person_id']} - {player['last_name']} {player['first_name']}")

        for staff_id in team['staff']:
            staff = self.get_person_by_id(staff_id, self.data_manager.load_staff())
            if staff:
                self.listbox_team_staff.insert(tk.END, f"{staff['person_id']} - {staff['last_name']} {staff['first_name']}")

        return self.entry_team_name  # initial focus

    def add_player_to_team(self):
        selected_indices = self.listbox_available_players.curselection()
        for index in selected_indices[::-1]:
            player = self.listbox_available_players.get(index)
            self.listbox_available_players.delete(index)
            self.listbox_team_players.insert(tk.END, player)

    def remove_player_from_team(self):
        selected_indices = self.listbox_team_players.curselection()
        for index in selected_indices[::-1]:
            player = self.listbox_team_players.get(index)
            self.listbox_team_players.delete(index)
            self.listbox_available_players.insert(tk.END, player)

    def add_staff_to_team(self):
        selected_indices = self.listbox_available_staff.curselection()
        for index in selected_indices[::-1]:
            staff = self.listbox_available_staff.get(index)
            self.listbox_available_staff.delete(index)
            self.listbox_team_staff.insert(tk.END, staff)

    def remove_staff_from_team(self):
        selected_indices = self.listbox_team_staff.curselection()
        for index in selected_indices[::-1]:
            staff = self.listbox_team_staff.get(index)
            self.listbox_team_staff.delete(index)
            self.listbox_available_staff.insert(tk.END, staff)

    def validate(self):
        try:
            self.new_team_name = self.entry_team_name.get()
            self.selected_team_players = [int(item.split(' - ')[0]) for item in self.listbox_team_players.get(0, tk.END)]
            self.selected_team_staff = [int(item.split(' - ')[0]) for item in self.listbox_team_staff.get(0, tk.END)]
            return True
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer des informations valides.")
            return False

    def apply(self):
        teams = self.data_manager.load_teams()
        for team in teams:
            if team['team_id'] == self.team_id:
                team['team_name'] = self.new_team_name
                team['players'] = self.selected_team_players
                team['staff'] = self.selected_team_staff
                break

        self.data_manager.save_teams(teams)
        self.callback()

    def get_team_by_id(self, team_id):
        teams = self.data_manager.load_teams()
        for team in teams:
            if team['team_id'] == team_id:
                return team
        return None

    def get_person_by_id(self, person_id, persons):
        for person in persons:
            if person['person_id'] == person_id:
                return person
        return None

