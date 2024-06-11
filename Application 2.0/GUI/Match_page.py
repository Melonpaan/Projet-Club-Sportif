from tkinter import Frame, Label, Button, Toplevel, Listbox, messagebox, StringVar, Entry
from tkinter.ttk import Combobox
import re
from tools import Tools
from classes.Match import Match
from classes.data_manager import DataManager
from classes.player import Player
from classes.team import Team

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

        Label(self.add_match_window, text="Mon équipe:").grid(row=1, column=0, padx=10, pady=10)
        self.team_var = StringVar()
        self.team_dropdown = Combobox(self.add_match_window, textvariable=self.team_var, values=self.get_team_names(), state='readonly')
        self.team_dropdown.grid(row=1, column=1, padx=10, pady=10)
        self.team_dropdown.bind("<<ComboboxSelected>>", lambda event: self.update_players_listbox(self.team_var.get()))

        self.entry_opponent = Tools.create_label_and_entry(self.add_match_window, "Adversaire:", 2)

        Label(self.add_match_window, text="Joueurs:").grid(row=3, column=0, padx=10, pady=10)
        self.players_listbox = Listbox(self.add_match_window, selectmode="multiple")
        self.players_listbox.grid(row=3, column=1, padx=10, pady=10)

        submit_button = Button(self.add_match_window, text="Soumettre", command=self.add_match, bg="#4CAF50", fg="white", font=("Helvetica", 12, "bold"))
        submit_button.grid(row=4, column=0, columnspan=2, pady=10)

    def get_team_names(self):
        """
        Retourne une liste des noms d'équipes disponibles.

        Returns:
            list: Une liste des noms d'équipes.
        """
        teams_data = DataManager.load_from_file('data/teams.json')
        if teams_data:
            return [team['name'] for team in teams_data]
        return []

    def update_players_listbox(self, selected_team):
        """
        Met à jour la listbox des joueurs en fonction de l'équipe sélectionnée.

        Args:
            selected_team (str): Le nom de l'équipe sélectionnée.
        """
        self.players_listbox.delete(0, "end")
        teams_data = DataManager.load_from_file('data/teams.json')
        players_data = DataManager.load_from_file('data/players.json')

        if teams_data and players_data:
            for team in teams_data:
                if team['name'] == selected_team:
                    player_ids = team['players']
                    for player_data in players_data:
                        if player_data['person_ID'] in player_ids:
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
        my_team = self.team_var.get()
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

            new_match.add_match(match_data)
            self.add_match_window.destroy()
            self.open_score_input_window(new_match)
        except FileNotFoundError as e:
            messagebox.showerror("Erreur", str(e))

    def open_score_input_window(self, match):
        """
        Ouvre une fenêtre pour saisir le score du match et les joueurs ayant marqué et fait des passes décisives.

        Args:
            match (Match): L'objet Match pour lequel les informations sont saisies.
        """
        self.score_input_window = Toplevel(self.master)
        self.score_input_window.title("Saisir le score du match")

        self.entry_score = Tools.create_label_and_entry(self.score_input_window, "Score (ex: 2-1):", 0)

        Button(self.score_input_window, text="Suivant", command=lambda: self.open_goal_scorer_window(match), bg="#4CAF50", fg="white", font=("Helvetica", 12, "bold")).grid(row=1, column=0, columnspan=2, pady=10)

    def open_goal_scorer_window(self, match):
        """
        Ouvre une fenêtre pour saisir les buteurs et les passeurs décisifs après avoir entré le score.

        Args:
            match (Match): L'objet Match pour lequel les informations sont saisies.
        """
        score_text = self.entry_score.get()
        self.score_input_window.destroy()

        try:
            my_team_score, opponent_score = map(int, score_text.split('-'))
            total_goals = my_team_score + opponent_score
        except ValueError:
            messagebox.showerror("Erreur", "Le score doit être au format 'X-Y'.")
            return

        self.goal_scorer_window = Toplevel(self.master)
        self.goal_scorer_window.title("Saisir les buteurs et passeurs décisifs")

        self.goal_scorer_entries = []
        self.assist_provider_entries = []
        self.minute_entries = []

        for i in range(my_team_score):
            Label(self.goal_scorer_window, text="Buteur:").grid(row=i, column=0, padx=10, pady=5)
            scorer_var = StringVar()
            scorer_dropdown = Combobox(self.goal_scorer_window, textvariable=scorer_var, values=match.players, state='readonly')
            scorer_dropdown.grid(row=i, column=1, padx=10, pady=5)
            self.goal_scorer_entries.append(scorer_var)

            Label(self.goal_scorer_window, text="Passeur décisif:").grid(row=i, column=2, padx=10, pady=5)
            assist_var = StringVar()
            assist_dropdown = Combobox(self.goal_scorer_window, textvariable=assist_var, values=match.players, state='readonly')
            assist_dropdown.grid(row=i, column=3, padx=10, pady=5)
            self.assist_provider_entries.append(assist_var)

            Label(self.goal_scorer_window, text="Minute:").grid(row=i, column=4, padx=10, pady=5)
            minute_entry = Entry(self.goal_scorer_window)
            minute_entry.grid(row=i, column=5, padx=10, pady=5)
            self.minute_entries.append(minute_entry)

        Button(self.goal_scorer_window, text="Soumettre", command=lambda: self.submit_match_statistics(match), bg="#4CAF50", fg="white", font=("Helvetica", 12, "bold")).grid(row=total_goals, column=0, columnspan=6, pady=10)

    def submit_match_statistics(self, match):
        """
        Soumet les statistiques du match et met à jour les données des joueurs dans le fichier JSON.

        Args:
            match (Match): L'objet Match pour lequel les informations sont soumises.
        """
        goal_scorers = [entry.get() for entry in self.goal_scorer_entries]
        assist_providers = [entry.get() for entry in self.assist_provider_entries]
        goal_minutes = [entry.get() for entry in self.minute_entries]

        players_data = DataManager.load_from_file('data/players.json')

        if players_data is None:
            messagebox.showerror("Erreur", "Les données des joueurs n'ont pas pu être chargées.")
            return

        for player_data in players_data:
            player_name = f"{player_data['first_name']} {player_data['last_name']}"

            #  compteur buts
            goals = sum(1 for scorer in goal_scorers if scorer == player_name)
            if goals > 0:
                if 'goals' not in player_data:
                    player_data['goals'] = 0
                player_data['goals'] += goals

            # compteur passe dé
            assists = sum(1 for assister in assist_providers if assister == player_name)
            if assists > 0:
                if 'assists' not in player_data:
                    player_data['assists'] = 0
                player_data['assists'] += assists


        DataManager.save_to_file(players_data, 'data/players.json')

        messagebox.showinfo("Information", "Les statistiques du match ont été soumises avec succès.")
        self.goal_scorer_window.destroy()


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
