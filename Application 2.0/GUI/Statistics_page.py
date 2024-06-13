from tkinter import Frame, Label, messagebox
from tkinter.ttk import Treeview
from classes.data_manager import DataManager

class StatisticsPage(Frame):
    """
    Classe pour gérer la page des statistiques des joueurs.
    Hérite de Frame pour créer un cadre Tkinter.
    """

    def __init__(self, master=None):
        """
        Initialise la fenêtre de la page des statistiques et crée les widgets nécessaires.

        Args:
            master: Référence à la fenêtre principale ou au parent Tkinter.
        """
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        """
        Crée les widgets de la page des statistiques, y compris le Treeview pour afficher les statistiques des joueurs.
        """
        self.label = Label(self, text="Statistiques des joueurs")
        self.label.grid(row=0, column=0, padx=10, pady=10)

        self.tree_statistics = Treeview(self, columns=(
            "Nom", "Prénom", "Buts", "Passes décisives", "Cartons jaunes", "Cartons rouges"), show='headings')
        self.tree_statistics.grid(row=1, column=0, padx=10, pady=10)

        # Définir les en-têtes des colonnes du Treeview
        for col in self.tree_statistics['columns']:
            self.tree_statistics.heading(col, text=col)

        self.update_statistics_treeview()

    def update_statistics_treeview(self):
        """
        Met à jour le Treeview des statistiques avec les données actuelles.
        """
        players_data = DataManager.load_from_file('data/players.json')
        if players_data:
            for player_data in players_data:
                self.tree_statistics.insert("", "end", values=(
                    player_data.get("last_name"),
                    player_data.get("first_name"),
                    player_data.get("goals", 0),
                    player_data.get("assists", 0),
                    player_data.get("yellow_cards", 0),
                    player_data.get("red_cards", 0)
                ))
        else:
            messagebox.showerror("Erreur", "Les données des joueurs n'ont pas pu être chargées.")
