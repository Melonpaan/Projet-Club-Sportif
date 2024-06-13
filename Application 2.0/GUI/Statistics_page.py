from tkinter import Frame, Label, Button, Entry, StringVar
from tkinter.ttk import Treeview
from classes.data_manager import DataManager

class StatisticsPage(Frame):
    """
    Classe pour gérer la page des statistiques des joueurs de l'application.
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
        Crée les widgets de la page des statistiques, y compris la barre de recherche et le tableau des statistiques.
        """
        # Container pr la recherche
        search_container = Frame(self)
        search_container.pack(fill='x', pady=10)

        search_label = Label(search_container, text="Rechercher par nom ou prénom:")
        search_label.pack(side='left', padx=5)

        self.search_var = StringVar()
        search_entry = Entry(search_container, textvariable=self.search_var)
        search_entry.pack(side='left', padx=5)

        search_button = Button(search_container, text="Rechercher", command=self.filter_statistics)
        search_button.pack(side='left', padx=5)

        # Container pr le tableau
        table_container = Frame(self)
        table_container.pack(expand=True, fill='both')

        columns = ("ID", "Nom", "Prénom", "Buts", "Passes décisives", "Cartons jaunes", "Cartons rouges")
        self.tree_statistics = Treeview(table_container, columns=columns, show='headings')

        for col in columns:
            self.tree_statistics.heading(col, text=col)

        self.tree_statistics.pack(expand=True, fill='both', padx=20, pady=20)

        self.load_statistics_data()

    def load_statistics_data(self, filter_text=""):
        """
        Charge les données des statistiques des joueurs dans le Treeview.

        Args:
            filter_text (str): Texte de filtrage pour rechercher les joueurs par nom ou prénom. Par défaut, une chaîne vide.
        """
        for item in self.tree_statistics.get_children():
            self.tree_statistics.delete(item)

        players_data = DataManager.load_from_file('data/players.json')
        if players_data:
            for player in players_data:
                if filter_text.lower() in player.get("last_name", "").lower() or filter_text.lower() in player.get("first_name", "").lower():
                    self.tree_statistics.insert("", "end", values=(
                        player.get("person_ID"),
                        player.get("last_name"),
                        player.get("first_name"),
                        player.get("goals", 0),
                        player.get("assists", 0),
                        player.get("yellow_cards", 0),
                        player.get("red_cards", 0)
                    ))

    def filter_statistics(self):
        """
        Filtre les statistiques des joueurs en fonction du texte de recherche saisi par l'utilisateur.
        """
        filter_text = self.search_var.get()
        self.load_statistics_data(filter_text)
