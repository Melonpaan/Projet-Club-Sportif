from tkinter import Frame, Label, Button, Toplevel, Listbox, messagebox
import re
from tools import Tools
from classes.Match import Match
from classes.data_manager import DataManager
from classes.player import Player

class MatchPage(Frame):
    """
    Classe pour gérer la page des matchs de l'application.
    Hérite de Frame pour créer un cadre Tkinter.
    """

    def __init__(self, master=None):
        """
        Initialise la fenêtre de la page des matchs et crée les widgets nécessaires.

        Args:
            master: Référence à la fenêtre principale ou au parent Tkinter.
        """
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        """
        Crée les widgets de la page des matchs, y compris les boutons pour ajouter et voir les matchs.
        """
        self.label = Label(self, text="Page des matchs")
        self.label.grid(row=0, column=0, padx=10, pady=10)

        Tools.create_button(self, "Ajouter un match", self.open_add_match_form, 1, 0)
        Tools.create_button(self, "Voir les matchs", self.view_matches, 2, 0)

    def open_add_match_form(self):
        """
        Ouvre une nouvelle fenêtre pour ajouter un nouveau match.
        """
        self.add_match_window = Toplevel(self.master)
        self.add_match_window.title("Ajouter un match")

        self.entry_date = Tools.create_label_and_entry(self.add_match_window, "Date (DD-MM-YYYY):", 0)
        self.entry_my_team = Tools.create_label_and_entry(self.add_match_window, "Mon équipe:", 1)
        self.entry_opponent = Tools.create_label_and_entry(self.add_match_window, "Adversaire:", 2)

        Label(self.add_match_window, text="Joueurs:").grid(row=3, column=0, padx=10, pady=10)
        self.players_listbox = Listbox(self.add_match_window, selectmode="multiple")
        self.players_listbox.grid(row=3, column=1, padx=10, pady=10)
        self.populate_players_listbox()

        Button(self.add_match_window, text="Soumettre", command=self.add_match).grid(row=4, column=0, columnspan=2, pady=10)

    def populate_players_listbox(self):
        """
        Remplit la listbox des joueurs avec les données actuelles des joueurs.
        """
        players_data = DataManager.load_from_file('data/players.json')
        if players_data is not None:
            for player_data in players_data:
                player = Player.from_dict(player_data)
                self.players_listbox.insert("end", f"{player.first_name} {player.last_name}")

    def validate_date(self, date_text):
        """
        Valide que la date est au format DD-MM-YYYY.

        Args:
            date_text (str): La date à valider.

        Returns:
            bool: True si la date est valide, False sinon.
        """
        pattern = r"^\d{2}-\d{2}-\d{4}$"
        if re.match(pattern, date_text):
            day, month, year = map(int, date_text.split('-'))
            if 1 <= day <= 31 and 1 <= month <= 12:
                return True
        return False

    def add_match(self):
        """
        Ajoute un nouveau match aux données des matchs après validation des champs et de la date.
        """
        date = self.entry_date.get()
        my_team = self.entry_my_team.get()
        opponent = self.entry_opponent.get()
        selected_players = [self.players_listbox.get(i) for i in self.players_listbox.curselection()]

        if not date or not my_team or not opponent or not selected_players:
            messagebox.showerror("Erreur", "Tous les champs doivent être remplis.")
            return

        if not self.validate_date(date):
            messagebox.showerror("Erreur", "La date doit être au format DD-MM-YYYY.")
            return

        new_match = Match(date, my_team, opponent, selected_players)
        match_data = {
            "date": date,
            "my_team": my_team,
            "opponent": opponent,
            "players": selected_players
        }

        try:
            # Ajout du match aux données de matches
            new_match.add_match(match_data)
            self.add_match_window.destroy()
        except FileNotFoundError as e:
            messagebox.showerror("Erreur", str(e))

    def view_matches(self):
        """
        Ouvre une nouvelle fenêtre pour afficher tous les matchs.
        """
        self.view_matches_window = Toplevel(self.master)
        self.view_matches_window.title("Voir les matchs")

        matches_data = DataManager.load_from_file('data/matches.json')
        if matches_data is not None:
            for index, match in enumerate(matches_data):
                Label(self.view_matches_window, text=f"{match['my_team']} vs {match['opponent']} - {match['date']}").grid(row=index, column=0, padx=10, pady=5)
                Button(self.view_matches_window, text="Voir plus", command=lambda m=match: self.view_match_details(m)).grid(row=index, column=1, padx=10, pady=5)

    def view_match_details(self, match):
        """
        Ouvre une nouvelle fenêtre pour afficher les détails d'un match spécifique.

        Args:
            match (dict): Les données du match à afficher.
        """
        details_window = Toplevel(self.master)
        details_window.title("Détails du match")

        Label(details_window, text=f"Date: {match['date']}").pack(padx=10, pady=5)
        Label(details_window, text=f"Mon équipe: {match['my_team']}").pack(padx=10, pady=5)
        Label(details_window, text=f"Adversaire: {match['opponent']}").pack(padx=10, pady=5)
        Label(details_window, text=f"Joueurs: {', '.join(match['players'])}").pack(padx=10, pady=5)
        Label(details_window, text=f"Score: 0").pack(padx=10, pady=5)
        Label(details_window, text=f"Buteur: | 0").pack(padx=10, pady=5)
        Label(details_window, text=f"Passeur décisif: | 0").pack(padx=10, pady=5)
        Label(details_window, text=f"Cartons jaunes: | 0").pack(padx=10, pady=5)
        Label(details_window, text=f"Cartons rouges: | 0").pack(padx=10, pady=5)
