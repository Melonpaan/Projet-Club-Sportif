# src/gui/player_tab.py
import tkinter as tk
from tkinter import ttk, messagebox
from src.gui.player_dialogs import AddPlayerDialog, EditPlayerDialog


class PlayerTab:
    def __init__(self, parent, data_manager):
        self.frame = ttk.Frame(parent)
        self.data_manager = data_manager

        self.create_widgets()
        self.populate_player_list()

    def create_widgets(self):
        self.tree = ttk.Treeview(self.frame, columns=("ID", "Nom", "Prénom", "Âge", "Poste", "Salaire"),
                                 show='headings')
        for col in ("ID", "Nom", "Prénom", "Âge", "Poste", "Salaire"):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        self.tree.pack(fill='both', expand=True)

        btn_frame = ttk.Frame(self.frame)
        btn_frame.pack(fill='x')

        self.add_btn = ttk.Button(btn_frame, text="Ajouter Joueur", command=self.add_player)
        self.add_btn.pack(side='left')

        self.edit_btn = ttk.Button(btn_frame, text="Modifier Joueur", command=self.edit_player)
        self.edit_btn.pack(side='left')

        self.delete_btn = ttk.Button(btn_frame, text="Supprimer Joueur", command=self.delete_player)
        self.delete_btn.pack(side='left')

    def populate_player_list(self):
        self.tree.delete(*self.tree.get_children())  # Clear existing entries
        players = self.data_manager.load_players()
        for player in players:
            self.tree.insert("", "end", values=(
            player['person_id'], player['last_name'], player['first_name'], player['age'], player['position'],
            player['salary']))

    def add_player(self):
        AddPlayerDialog(self.frame, self.data_manager, self.populate_player_list)

    def edit_player(self):
        selected_item = self.tree.selection()
        if selected_item:
            player_id = self.tree.item(selected_item)["values"][0]
            EditPlayerDialog(self.frame, self.data_manager, player_id, self.populate_player_list)
        else:
            messagebox.showwarning("Attention", "Veuillez sélectionner un joueur à modifier.")

    def delete_player(self):
        selected_item = self.tree.selection()
        if selected_item:
            player_id = self.tree.item(selected_item)["values"][0]
            players = self.data_manager.load_players()
            players = [player for player in players if player['person_id'] != player_id]
            self.data_manager.save_players(players)
            self.populate_player_list()
        else:
            messagebox.showwarning("Attention", "Veuillez sélectionner un joueur à supprimer.")
