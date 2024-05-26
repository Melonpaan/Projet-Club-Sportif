# src/gui/gui_manager.py
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import tkinter as tk
from tkinter import ttk
from src.controller.data_manager import DataManager
from src.gui.player_tab import PlayerTab
from src.gui.staff_tab import StaffTab
from src.gui.team_tab import TeamTab  # Importer le nouvel onglet des équipes


class GUIManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Football Club Manager")

        self.data_manager = DataManager('data')

        self.create_menu()
        self.create_tabs()

    def create_menu(self):
        menubar = tk.Menu(self.root)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Nouveau")
        file_menu.add_command(label="Ouvrir")
        file_menu.add_command(label="Sauvegarder")
        file_menu.add_separator()
        file_menu.add_command(label="Quitter", command=self.root.quit)
        menubar.add_cascade(label="Fichier", menu=file_menu)

        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="À propos")
        help_menu.add_command(label="Aide")
        menubar.add_cascade(label="Aide", menu=help_menu)

        self.root.config(menu=menubar)

    def create_tabs(self):
        tab_control = ttk.Notebook(self.root)

        self.tab_players = PlayerTab(tab_control, self.data_manager)
        tab_control.add(self.tab_players.frame, text='Joueurs')

        self.tab_staff = StaffTab(tab_control, self.data_manager)
        tab_control.add(self.tab_staff.frame, text='Staff')

        self.tab_teams = TeamTab(tab_control, self.data_manager)  # Ajouter l'onglet Équipes
        tab_control.add(self.tab_teams.frame, text='Équipes')

        # Ajouter des tabs pour Matchs, Entraînements, etc.

        tab_control.pack(expand=1, fill='both')


if __name__ == "__main__":
    root = tk.Tk()
    app = GUIManager(root)
    root.mainloop()
