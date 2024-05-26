# src/gui/team_tab.py
import tkinter as tk
from tkinter import ttk, messagebox
from src.gui.team_dialogs import AddTeamDialog, EditTeamDialog


class TeamTab:
    def __init__(self, parent, data_manager):
        self.frame = ttk.Frame(parent)
        self.data_manager = data_manager

        self.create_widgets()
        self.populate_team_list()

    def create_widgets(self):
        self.tree = ttk.Treeview(self.frame, columns=("ID", "Nom de l'équipe", "Joueurs", "Staff"), show='headings')
        for col in ("ID", "Nom de l'équipe", "Joueurs", "Staff"):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)
        self.tree.pack(fill='both', expand=True)

        btn_frame = ttk.Frame(self.frame)
        btn_frame.pack(fill='x')

        self.add_btn = ttk.Button(btn_frame, text="Ajouter Équipe", command=self.add_team)
        self.add_btn.pack(side='left')

        self.edit_btn = ttk.Button(btn_frame, text="Modifier Équipe", command=self.edit_team)
        self.edit_btn.pack(side='left')

        self.delete_btn = ttk.Button(btn_frame, text="Supprimer Équipe", command=self.delete_team)
        self.delete_btn.pack(side='left')

    def populate_team_list(self):
        self.tree.delete(*self.tree.get_children())  # Clear existing entries
        teams = self.data_manager.load_teams()
        for team in teams:
            players = ', '.join(str(player_id) for player_id in team['players'])
            staff = ', '.join(str(staff_id) for staff_id in team['staff'])
            self.tree.insert("", "end", values=(team['team_id'], team['team_name'], players, staff))

    def add_team(self):
        AddTeamDialog(self.frame, self.data_manager, self.populate_team_list)

    def edit_team(self):
        selected_item = self.tree.selection()
        if selected_item:
            team_id = self.tree.item(selected_item)["values"][0]
            EditTeamDialog(self.frame, self.data_manager, team_id, self.populate_team_list)
        else:
            messagebox.showwarning("Attention", "Veuillez sélectionner une équipe à modifier.")

    def delete_team(self):
        selected_item = self.tree.selection()
        if selected_item:
            team_id = self.tree.item(selected_item)["values"][0]
            teams = self.data_manager.load_teams()
            teams = [team for team in teams if team['team_id'] != team_id]
            self.data_manager.save_teams(teams)
            self.populate_team_list()
        else:
            messagebox.showwarning("Attention", "Veuillez sélectionner une équipe à supprimer.")
