from tkinter import Frame, Label, Button, Toplevel, Listbox, messagebox, StringVar, Entry
from tkinter.ttk import Combobox
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

        Label(self.add_match_window, text="Mon équipe:").grid(row=1, column=0, padx=10, pady=10)
        self.team_var = StringVar()
        self.team_dropdown = Combobox(self.add_match_window, textvariable=self.team_var, values=self.get_team_names(), state='readonly')
        self.team_dropdown.grid(row=1, column=1, padx=10, pady=10)
        self.team_dropdown.bind("<<ComboboxSelected>>", lambda event: self.update_players_listbox(self.team_var.get()))

        self.entry_opponent = Tools.create_label_and_entry(self.add_match_window, "Adversaire:", 2)

        Label(self.add_match_window, text="Joueurs:").grid(row=3, column=0, padx=10, pady=10)
        self.players_listbox = Listbox(self.add_match_window, selectmode="multiple")
        self.players_listbox.grid(row=3, column=1, padx=10, pady=10)

        submit_button = Button(self.add_match_window, text="Soumettre", command=self.add_match)
        submit_button.grid(row=4, column=0, columnspan=2, pady=10)

    def delete_match(self, match):
        """
         Supprime un match et met à jour les fichiers JSON correspondants.

         Args:
            match (Match): Le match à supprimer.
        """
        matches_data = DataManager.load_from_file('data/matches.json')
        if matches_data is not None:
            matches_data = [m for m in matches_data if m['match_id'] != match.match_id]
            DataManager.save_to_file(matches_data, 'data/matches.json')

        players_data = DataManager.load_from_file('data/players.json')
        if players_data is not None:
            for player_data in players_data:
                player_name = f"{player_data['first_name']} {player_data['last_name']}"
                if 'goals' in player_data:
                    player_data['goals'] -= sum(1 for stat in match.statistics if stat['scorer'] == player_name)
                if 'assists' in player_data:
                    player_data['assists'] -= sum(1 for stat in match.statistics if stat['assister'] == player_name)
                if 'yellow_cards' in player_data:
                    player_data['yellow_cards'] -= 1 if player_name in match.yellow_cards else 0
                if 'red_cards' in player_data:
                    player_data['red_cards'] -= 1 if player_name in match.red_cards else 0
            DataManager.save_to_file(players_data, 'data/players.json')

        messagebox.showinfo("Information", "Le match a été supprimé avec succès.")
        self.view_matches_window.destroy()
        self.view_matches()

    def open_edit_match_form(self, match):
        """
        Ouvre une fenêtre pour modifier un match existant.

        Args:
            match (Match): Le match à modifier.
        """
        self.edit_match_window = Toplevel(self.master)
        self.edit_match_window.title("Modifier le match")

        self.entry_date = Tools.create_label_and_entry(self.edit_match_window, "Date (DD-MM-YYYY):", 0, match.date)

        Label(self.edit_match_window, text="Mon équipe:").grid(row=1, column=0, padx=10, pady=10)
        self.team_var = StringVar(value=match.my_team)
        self.team_dropdown = Combobox(self.edit_match_window, textvariable=self.team_var, values=self.get_team_names(), state='readonly')
        self.team_dropdown.grid(row=1, column=1, padx=10, pady=10)
        self.team_dropdown.bind("<<ComboboxSelected>>", lambda event: self.update_players_listbox(self.team_var.get()))

        self.entry_opponent = Tools.create_label_and_entry(self.edit_match_window, "Adversaire:", 2, match.opponent)

        Label(self.edit_match_window, text="Joueurs:").grid(row=3, column=0, padx=10, pady=10)
        self.players_listbox = Listbox(self.edit_match_window, selectmode="multiple")
        self.players_listbox.grid(row=3, column=1, padx=10, pady=10)
        self.update_players_listbox(match.my_team)

        for player in match.players:
            idx = self.players_listbox.get(0, 'end').index(player)
            self.players_listbox.selection_set(idx)

        Label(self.edit_match_window, text="Score (ex: 2-1):").grid(row=4, column=0, padx=10, pady=10)
        self.entry_score = Entry(self.edit_match_window)
        self.entry_score.insert(0, match.score if match.score else '')
        self.entry_score.grid(row=4, column=1, padx=10, pady=10)

        Button(self.edit_match_window, text="Suivant", command=lambda: self.open_goal_scorer_window(match, edit=True),).grid(row=5, column=0, columnspan=2, pady=10)

    def edit_match(self, match):
        """
        Modifie un match existant et met à jour les fichiers JSON correspondants.

        Args:
            match (Match): Le match à modifier.
        """
        date = self.entry_date.get()
        my_team = self.team_var.get()
        opponent = self.entry_opponent.get()
        selected_players = [self.players_listbox.get(i) for i in self.players_listbox.curselection()]
        score_text = self.entry_score.get()

        if not date or not my_team or not opponent or not selected_players or not score_text:
            messagebox.showerror("Erreur", "Tous les champs doivent être remplis.")
            return

        if not self.validate_date(date):
            messagebox.showerror("Erreur", "La date doit être au format DD-MM-YYYY.")
            return

        match_data = match.to_dict()
        match_data.update({
            "date": date,
            "my_team": my_team,
            "opponent": opponent,
            "players": selected_players,
            "score": score_text
        })

        matches_data = DataManager.load_from_file('data/matches.json')
        if matches_data is not None:
            for i, m in enumerate(matches_data):
                if m['match_id'] == match.match_id:
                    matches_data[i] = match_data
                    break
            DataManager.save_to_file(matches_data, 'data/matches.json')

        self.edit_match_window.destroy()
        self.view_matches_window.destroy()
        self.open_goal_scorer_window(match, edit=True)

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

        match_id = self.generate_match_id()  # Générer un ID unique pour le match
        new_match = Match(match_id, date, my_team, opponent, selected_players)
        match_data = new_match.to_dict()

        try:
            new_match.add_match(match_data)
            self.add_match_window.destroy()
            self.open_score_input_window(new_match)
        except FileNotFoundError as e:
            messagebox.showerror("Erreur", str(e))

    def generate_match_id(self):
        """
        Génère un ID unique pour un match.

        Returns:
            int: Un ID unique pour le match.
        """
        matches_data = DataManager.load_from_file('data/matches.json') or []
        match_ids = [match["match_id"] for match in matches_data if "match_id" in match]
        if not match_ids:
            return 1
        return max(match_ids) + 1

    def open_score_input_window(self, match):
        """
        Ouvre une fenêtre pour saisir le score du match et les joueurs ayant marqué et fait des passes décisives.

        Args:
            match (Match): L'objet Match pour lequel les informations sont saisies.
        """
        self.score_input_window = Toplevel(self.master)
        self.score_input_window.title("Saisir le score du match")

        self.entry_score = Tools.create_label_and_entry(self.score_input_window, "Score (ex: 2-1):", 0)

        Button(self.score_input_window, text="Suivant", command=lambda: self.open_goal_scorer_window(match)).grid(row=1, column=0, columnspan=2, pady=10)

    def open_goal_scorer_window(self, match, edit=False):
        """
        Ouvre une fenêtre pour saisir les buteurs et les passeurs décisifs après avoir entré le score.

        Args:
            match (Match): L'objet Match pour lequel les informations sont saisies.
            edit (bool): Indique si la fenêtre est ouverte pour modification.
        """
        if edit:
            score_text = self.entry_score.get()
        else:
            score_text = self.entry_score.get()
            self.score_input_window.destroy()

        try:
            my_team_score, opponent_score = map(int, score_text.split('-'))
        except ValueError:
            messagebox.showerror("Erreur", "Le score doit être au format 'X-Y'.")
            return

        self.goal_scorer_window = Toplevel(self.master)
        self.goal_scorer_window.title("Saisir les buteurs et passeurs décisifs")

        self.goal_scorer_entries = []
        self.assist_provider_entries = []
        self.minute_entries = []

        if edit:
            existing_statistics = match.statistics
            players = match.players
        else:
            existing_statistics = []
            players = match.players

        for i in range(my_team_score):
            Label(self.goal_scorer_window, text="Buteur:").grid(row=i, column=0, padx=10, pady=5)
            scorer_var = StringVar(value=existing_statistics[i]['scorer'] if i < len(existing_statistics) else "")
            scorer_dropdown = Combobox(self.goal_scorer_window, textvariable=scorer_var, values=players, state='readonly')
            scorer_dropdown.grid(row=i, column=1, padx=10, pady=5)
            self.goal_scorer_entries.append(scorer_var)

            Label(self.goal_scorer_window, text="Passeur décisif:").grid(row=i, column=2, padx=10, pady=5)
            assist_var = StringVar(value=existing_statistics[i]['assister'] if i < len(existing_statistics) else "")
            assist_dropdown = Combobox(self.goal_scorer_window, textvariable=assist_var, values=players, state='readonly')
            assist_dropdown.grid(row=i, column=3, padx=10, pady=5)
            self.assist_provider_entries.append(assist_var)

            Label(self.goal_scorer_window, text="Minute:").grid(row=i, column=4, padx=10, pady=5)
            minute_var = StringVar(value=existing_statistics[i]['minute'] if i < len(existing_statistics) else "")
            minute_entry = Entry(self.goal_scorer_window, textvariable=minute_var)
            minute_entry.grid(row=i, column=5, padx=10, pady=5)
            self.minute_entries.append(minute_var)

        Button(self.goal_scorer_window, text="Soumettre", command=lambda: self.submit_match_statistics(match, score_text, edit)).grid(row=my_team_score, column=0, columnspan=6, pady=10)

    def submit_match_statistics(self, match, score_text, edit=False):
        """
        Soumet les statistiques du match et met à jour les données des joueurs dans le fichier JSON.

        Args:
            match (Match): L'objet Match pour lequel les informations sont soumises.
            score_text (str): Le score du match.
            edit (bool): Indique si les statistiques sont soumises pour une modification.
        """
        goal_scorers = [entry.get() for entry in self.goal_scorer_entries]
        assist_providers = [entry.get() for entry in self.assist_provider_entries]
        goal_minutes = [entry.get() for entry in self.minute_entries]

        players_data = DataManager.load_from_file('data/players.json')

        if players_data is None:
            messagebox.showerror("Erreur", "Les données des joueurs n'ont pas pu être chargées.")
            return

        if edit:
            for stat in match.statistics:
                player_name = stat['scorer']
                assister_name = stat['assister']
                for player_data in players_data:
                    full_name = f"{player_data['first_name']} {player_data['last_name']}"
                    if full_name == player_name:
                        player_data['goals'] = player_data.get('goals', 0) - 1
                    if full_name == assister_name:
                        player_data['assists'] = player_data.get('assists', 0) - 1

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

        # Charge les données actuelles des matchs
        matches_data = DataManager.load_from_file('data/matches.json')
        if matches_data is not None:
            for i, m in enumerate(matches_data):
                if m['match_id'] == match.match_id:
                    matches_data[i]['score'] = score_text
                    matches_data[i]['statistics'] = [
                        {"scorer": scorer, "assister": assister, "minute": minute}
                        for scorer, assister, minute in zip(goal_scorers, assist_providers, goal_minutes)
                    ]
                    break
            DataManager.save_to_file(matches_data, 'data/matches.json')

        self.goal_scorer_window.destroy()
        self.open_card_input_window(match, edit)

    def open_card_input_window(self, match, edit=False):
        """
        Ouvre une fenêtre pour saisir les cartons jaunes et rouges après avoir entré les buteurs et passeurs.

        Args:
            match (Match): Le match pour lequel les informations sont saisies.
            edit (bool): Indique si la fenêtre est ouverte pour modification.
        """
        self.card_input_window = Toplevel(self.master)
        self.card_input_window.title("Saisir les cartons")

        Label(self.card_input_window, text="Cartons jaunes").grid(row=0, column=1, padx=10, pady=5)
        Label(self.card_input_window, text="Cartons rouges").grid(row=0, column=2, padx=10, pady=5)

        self.yellow_card_entries = []
        self.red_card_entries = []

        for i, player in enumerate(match.players):
            Label(self.card_input_window, text=player).grid(row=i+1, column=0, padx=10, pady=5)
            yellow_var = StringVar(value="Yes" if player in match.yellow_cards else "No")
            red_var = StringVar(value="Yes" if player in match.red_cards else "No")

            yellow_dropdown = Combobox(self.card_input_window, textvariable=yellow_var, values=["Yes", "No"], state='readonly')
            yellow_dropdown.grid(row=i+1, column=1, padx=10, pady=5)
            self.yellow_card_entries.append((player, yellow_var))

            red_dropdown = Combobox(self.card_input_window, textvariable=red_var, values=["Yes", "No"], state='readonly')
            red_dropdown.grid(row=i+1, column=2, padx=10, pady=5)
            self.red_card_entries.append((player, red_var))

        Button(self.card_input_window, text="Soumettre", command=lambda: self.submit_card_statistics(match, edit)).grid(row=len(match.players)+1, column=0, columnspan=3, pady=10)

    def submit_card_statistics(self, match, edit=False):
        """
        Soumet les statistiques des cartons et met à jour les données des joueurs dans le fichier JSON.

        Args:
            match (Match): Le match pour lequel les informations sont soumises.
            edit (bool): Indique si les statistiques sont soumises pour une modification.
        """
        yellow_cards = [player for player, var in self.yellow_card_entries if var.get() == "Yes"]
        red_cards = [player for player, var in self.red_card_entries if var.get() == "Yes"]

        players_data = DataManager.load_from_file('data/players.json')

        if players_data is None:
            messagebox.showerror("Erreur", "Les données des joueurs n'ont pas pu être chargées.")
            return

        if edit:
            for player_data in players_data:
                player_name = f"{player_data['first_name']} {player_data['last_name']}"
                if player_name in match.yellow_cards:
                    player_data['yellow_cards'] = player_data.get('yellow_cards', 0) - 1
                if player_name in match.red_cards:
                    player_data['red_cards'] = player_data.get('red_cards', 0) - 1

        for player_data in players_data:
            player_name = f"{player_data['first_name']} {player_data['last_name']}"
            if player_name in yellow_cards:
                player_data['yellow_cards'] = player_data.get('yellow_cards', 0) + 1
            if player_name in red_cards:
                player_data['red_cards'] = player_data.get('red_cards', 0) + 1

        DataManager.save_to_file(players_data, 'data/players.json')

        # Charge les données actuelles des matchs
        matches_data = DataManager.load_from_file('data/matches.json')
        if matches_data is not None:
            for i, m in enumerate(matches_data):
                if m['match_id'] == match.match_id:
                    matches_data[i]['yellow_cards'] = yellow_cards
                    matches_data[i]['red_cards'] = red_cards
                    break
            DataManager.save_to_file(matches_data, 'data/matches.json')

        messagebox.showinfo("Information", "Les statistiques du match ont été soumises avec succès.")
        self.card_input_window.destroy()

    def view_matches(self):
        """
        Ouvre une nouvelle fenêtre pour afficher tous les matchs.
        """
        self.view_matches_window = Toplevel(self.master)
        self.view_matches_window.title("Voir les matchs")

        matches_data = DataManager.load_from_file('data/matches.json')
        if matches_data:
            for index, match in enumerate(matches_data):
                match_obj = Match.from_dict(match)
                Label(self.view_matches_window, text=f"{match_obj.my_team} vs {match_obj.opponent} - {match_obj.date}").grid(row=index, column=0, padx=10, pady=5)
                Button(self.view_matches_window, text="Voir plus", command=lambda m=match_obj: self.view_match_details(m)).grid(row=index, column=1, padx=10, pady=5)
                Button(self.view_matches_window, text="Modifier", command=lambda m=match_obj: self.open_edit_match_form(m)).grid(row=index, column=2, padx=10, pady=5)
                Button(self.view_matches_window, text="Supprimer", command=lambda m=match_obj: self.delete_match(m)).grid(row=index, column=3, padx=10, pady=5)
        else:
            messagebox.showerror("Erreur", "Aucun match enregistré pour cette saison.")

    def view_match_details(self, match):
        """
        Ouvre une nouvelle fenêtre pour afficher les détails d'un match spécifique.

        Args:
            match (Match): Les données du match à afficher.
        """
        details_window = Toplevel(self.master)
        details_window.title("Détails du match")

        Label(details_window, text=f"Date: {match.date}").pack(padx=10, pady=5)
        Label(details_window, text=f"Mon équipe: {match.my_team}").pack(padx=10, pady=5)
        Label(details_window, text=f"Adversaire: {match.opponent}").pack(padx=10, pady=5)
        Label(details_window, text=f"Joueurs: {', '.join(match.players)}").pack(padx=10, pady=5)
        Label(details_window, text=f"Score: {match.score if match.score else 'N/A'}").pack(padx=10, pady=5)
        for stat in match.statistics:
            Label(details_window, text=f"Buteur: {stat['scorer']}, Passeur: {stat['assister']}, Minute: {stat['minute']}").pack(padx=10, pady=5)
        Label(details_window, text=f"Cartons jaunes: {', '.join(match.yellow_cards)}").pack(padx=10, pady=5)
        Label(details_window, text=f"Cartons rouges: {', '.join(match.red_cards)}").pack(padx=10, pady=5)
