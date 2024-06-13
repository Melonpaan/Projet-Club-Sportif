from tkinter import Frame, Label, Button, Toplevel, Listbox, messagebox, StringVar
from tkinter.ttk import Combobox
import re
from tools import Tools
from classes.Training import Training
from classes.data_manager import DataManager
from classes.player import Player

class TrainingPage(Frame):
    """
    Classe pour gérer la page des entraînements de l'application.
    Hérite de Frame pour créer un cadre Tkinter.
    """

    def __init__(self, master=None):
        """
        Initialise la fenêtre de la page des entraînements et crée les widgets nécessaires.

        Args:
            master: Référence à la fenêtre principale ou au parent Tkinter.
        """
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        """
        Crée les widgets de la page des entraînements, y compris les boutons pour ajouter et voir les entraînements.
        """
        self.label = Label(self, text="Page des entraînements")
        self.label.grid(row=0, column=0, padx=10, pady=10)

        Tools.create_button(self, "Ajouter un entraînement", self.open_add_training_form, 1, 0)
        Tools.create_button(self, "Voir les entraînements", self.view_trainings, 2, 0)

    def open_add_training_form(self):
        """
        Ouvre une nouvelle fenêtre pour ajouter un nouvel entraînement.
        """
        self.add_training_window = Toplevel(self.master)
        self.add_training_window.title("Ajouter un entraînement")

        self.entry_date = Tools.create_label_and_entry(self.add_training_window, "Date (DD-MM-YYYY):", 0)

        Label(self.add_training_window, text="Mon équipe:").grid(row=1, column=0, padx=10, pady=10)
        self.team_var = StringVar()
        self.team_dropdown = Combobox(self.add_training_window, textvariable=self.team_var, values=self.get_team_names(), state='readonly')
        self.team_dropdown.grid(row=1, column=1, padx=10, pady=10)
        self.team_dropdown.bind("<<ComboboxSelected>>", lambda event: self.update_players_listbox(self.team_var.get()))

        self.entry_location = Tools.create_label_and_entry(self.add_training_window, "Lieu:", 2)

        Label(self.add_training_window, text="Type d'entraînement:").grid(row=3, column=0, padx=10, pady=10)
        self.training_type_var = StringVar()
        self.training_type_dropdown = Combobox(self.add_training_window, textvariable=self.training_type_var, values=[
            "Entrainement aux tirs", "Entrainement aux passes", "Entrainements défensif", "Entrainement cardio", "Entrainement technique", "Entrainement musculaire", "Entrainement complet"
        ], state='readonly')
        self.training_type_dropdown.grid(row=3, column=1, padx=10, pady=10)

        Label(self.add_training_window, text="Joueurs:").grid(row=4, column=0, padx=10, pady=10)
        self.players_listbox = Listbox(self.add_training_window, selectmode="multiple")
        self.players_listbox.grid(row=4, column=1, padx=10, pady=10)

        submit_button = Button(self.add_training_window, text="Soumettre", command=self.add_training, bg="#4CAF50", fg="white", font=("Helvetica", 12, "bold"))
        submit_button.grid(row=5, column=0, columnspan=2, pady=10)

    def delete_training(self, training):
        """
        Supprime un entraînement et met à jour les fichiers JSON correspondants.

        Args:
            training (Training): L'entraînement à supprimer.
        """
        trainings_data = DataManager.load_from_file('data/trainings.json')
        if trainings_data is not None:
            trainings_data = [t for t in trainings_data if t['training_id'] != training.training_id]
            DataManager.save_to_file(trainings_data, 'data/trainings.json')

        messagebox.showinfo("Information", "L'entraînement a été supprimé avec succès.")
        self.view_trainings_window.destroy()
        self.view_trainings()

    def open_edit_training_form(self, training):
        """
        Ouvre une fenêtre pour modifier un entraînement existant.

        Args:
            training (Training): L'entraînement à modifier.
        """
        self.edit_training_window = Toplevel(self.master)
        self.edit_training_window.title("Modifier l'entraînement")

        self.entry_date = Tools.create_label_and_entry(self.edit_training_window, "Date (DD-MM-YYYY):", 0, training.date)

        Label(self.edit_training_window, text="Mon équipe:").grid(row=1, column=0, padx=10, pady=10)
        self.team_var = StringVar(value=training.my_team)
        self.team_dropdown = Combobox(self.edit_training_window, textvariable=self.team_var, values=self.get_team_names(), state='readonly')
        self.team_dropdown.grid(row=1, column=1, padx=10, pady=10)
        self.team_dropdown.bind("<<ComboboxSelected>>", lambda event: self.update_players_listbox(self.team_var.get()))

        self.entry_location = Tools.create_label_and_entry(self.edit_training_window, "Lieu:", 2, training.location)

        Label(self.edit_training_window, text="Type d'entraînement:").grid(row=3, column=0, padx=10, pady=10)
        self.training_type_var = StringVar(value=training.training_type)
        self.training_type_dropdown = Combobox(self.edit_training_window, textvariable=self.training_type_var, values=[
            "Entrainement aux tirs", "Entrainement aux passes", "Entrainements défensif", "Entrainement cardio", "Entrainement technique", "Entrainement musculaire", "Entrainement complet"
        ], state='readonly')
        self.training_type_dropdown.grid(row=3, column=1, padx=10, pady=10)

        Label(self.edit_training_window, text="Joueurs:").grid(row=4, column=0, padx=10, pady=10)
        self.players_listbox = Listbox(self.edit_training_window, selectmode="multiple")
        self.players_listbox.grid(row=4, column=1, padx=10, pady=10)
        self.update_players_listbox(training.my_team)

        for player in training.players:
            idx = self.players_listbox.get(0, 'end').index(player)
            self.players_listbox.selection_set(idx)

        Button(self.edit_training_window, text="Suivant", command=lambda: self.open_player_rating_window(training, edit=True), bg="#4CAF50", fg="white", font=("Helvetica", 12, "bold")).grid(row=5, column=0, columnspan=2, pady=10)

    def edit_training(self, training):
        """
        Modifie un entraînement existant et met à jour les fichiers JSON correspondants.

        Args:
            training (Training): L'entraînement à modifier.
        """
        date = self.entry_date.get()
        my_team = self.team_var.get()
        location = self.entry_location.get()
        training_type = self.training_type_var.get()
        selected_players = [self.players_listbox.get(i) for i in self.players_listbox.curselection()]

        if not date or not my_team or not location or not training_type or not selected_players:
            messagebox.showerror("Erreur", "Tous les champs doivent être remplis.")
            return

        if not self.validate_date(date):
            messagebox.showerror("Erreur", "La date doit être au format DD-MM-YYYY.")
            return

        training_data = {
            "training_id": training.training_id,
            "date": date,
            "my_team": my_team,
            "location": location,
            "training_type": training_type,
            "players": selected_players
        }

        trainings_data = DataManager.load_from_file('data/trainings.json')
        if trainings_data is not None:
            for i, t in enumerate(trainings_data):
                if t['training_id'] == training.training_id:
                    trainings_data[i] = training_data
                    break
            DataManager.save_to_file(trainings_data, 'data/trainings.json')

        self.edit_training_window.destroy()
        self.view_trainings_window.destroy()
        self.open_player_rating_window(training, edit=True)

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
                            self.players_listbox.insert("end", f"{player.first_name} {player.last_name} ({player.position})")

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

    def add_training(self):
        """
        Ajoute un nouvel entraînement aux données des entraînements après validation des champs et de la date.
        """
        date = self.entry_date.get()
        my_team = self.team_var.get()
        location = self.entry_location.get()
        training_type = self.training_type_var.get()
        selected_players = [self.players_listbox.get(i) for i in self.players_listbox.curselection()]

        if not date or not my_team or not location or not training_type or not selected_players:
            messagebox.showerror("Erreur", "Tous les champs doivent être remplis.")
            return

        if not self.validate_date(date):
            messagebox.showerror("Erreur", "La date doit être au format DD-MM-YYYY.")
            return

        training_id = self.generate_training_id()
        new_training = Training(training_id, date, my_team, location, training_type, selected_players)
        training_data = new_training.to_dict()

        try:
            new_training.add_training(training_data)
            self.add_training_window.destroy()
            self.open_player_rating_window(new_training)
        except FileNotFoundError as e:
            messagebox.showerror("Erreur", str(e))

    def generate_training_id(self):
        """
        Génère un ID unique pour un entraînement.

        Returns:
            int: Un ID unique pour l'entraînement.
        """
        trainings_data = DataManager.load_from_file('data/trainings.json') or []
        if not trainings_data:
            return 1
        max_id = max(training.get("training_id", 0) for training in trainings_data)
        return max_id + 1

    def open_player_rating_window(self, training, edit=False):
        """
        Ouvre une fenêtre pour donner une note aux joueurs après l'entraînement.

        Args:
            training (Training): L'objet Training pour lequel les informations sont saisies.
            edit (bool): Indique si la fenêtre est ouverte pour modification.
        """
        self.rating_window = Toplevel(self.master)
        self.rating_window.title("Évaluation des joueurs")

        self.rating_entries = []

        existing_ratings = training.ratings if edit else {}

        for i, player in enumerate(training.players):
            Label(self.rating_window, text=player).grid(row=i, column=0, padx=10, pady=5)
            rating_var = StringVar(value=str(existing_ratings.get(player, "")))
            rating_dropdown = Combobox(self.rating_window, textvariable=rating_var, values=[1, 2, 3, 4, 5], state='readonly')
            rating_dropdown.grid(row=i, column=1, padx=10, pady=5)
            self.rating_entries.append((player, rating_var))

        Button(self.rating_window, text="Soumettre", command=lambda: self.submit_player_ratings(training, edit), bg="#4CAF50", fg="white", font=("Helvetica", 12, "bold")).grid(row=len(training.players), column=0, columnspan=2, pady=10)

    def submit_player_ratings(self, training, edit=False):
        """
        Soumet les évaluations des joueurs et met à jour les données des entraînements dans le fichier JSON.

        Args:
            training (Training): L'objet Training pour lequel les informations sont soumises.
            edit (bool): Indique si les évaluations sont soumises pour une modification.
        """
        player_ratings = {}
        for player, rating in self.rating_entries:
            try:
                player_ratings[player] = int(rating.get())
            except ValueError:
                messagebox.showerror("Erreur", "Toutes les notes doivent être des nombres entiers.")
                return

        if edit:
            training.ratings = player_ratings
        else:
            training.ratings.update(player_ratings)

        trainings_data = DataManager.load_from_file('data/trainings.json') or []
        for i, training_data in enumerate(trainings_data):
            if training_data['training_id'] == training.training_id:
                trainings_data[i] = training.to_dict()
                break
        else:
            trainings_data.append(training.to_dict())

        DataManager.save_to_file(trainings_data, 'data/trainings.json')

        messagebox.showinfo("Information", "Les évaluations des joueurs ont été soumises avec succès.")
        self.rating_window.destroy()

    def view_trainings(self):
        """
        Ouvre une nouvelle fenêtre pour afficher tous les entraînements.
        """
        self.view_trainings_window = Toplevel(self.master)
        self.view_trainings_window.title("Voir les entraînements")

        trainings_data = DataManager.load_from_file('data/trainings.json')
        if trainings_data is not None:
            for index, training in enumerate(trainings_data):
                training_obj = Training.from_dict(training)
                Label(self.view_trainings_window, text=f"{training['my_team']} - {training['location']} - {training['date']}").grid(row=index, column=0, padx=10, pady=5)
                Button(self.view_trainings_window, text="Voir plus", command=lambda t=training_obj: self.view_training_details(t)).grid(row=index, column=1, padx=10, pady=5)
                Button(self.view_trainings_window, text="Modifier", command=lambda t=training_obj: self.open_edit_training_form(t)).grid(row=index, column=2, padx=10, pady=5)
                Button(self.view_trainings_window, text="Supprimer", command=lambda t=training_obj: self.delete_training(t)).grid(row=index, column=3, padx=10, pady=5)

    def view_training_details(self, training):
        """
        Ouvre une nouvelle fenêtre pour afficher les détails d'un entraînement spécifique.

        Args:
            training (Training): Les données de l'entraînement à afficher.
        """
        details_window = Toplevel(self.master)
        details_window.title("Détails de l'entraînement")

        Label(details_window, text=f"Date: {training.date}").pack(padx=10, pady=5)
        Label(details_window, text=f"Mon équipe: {training.my_team}").pack(padx=10, pady=5)
        Label(details_window, text=f"Lieu: {training.location}").pack(padx=10, pady=5)
        Label(details_window, text=f"Type d'entraînement: {training.training_type}").pack(padx=10, pady=5)

        if training.ratings:
            Label(details_window, text="Évaluations:").pack(padx=10, pady=5)
            for player, rating in training.ratings.items():
                Label(details_window, text=f"{player}: {rating}").pack(padx=10, pady=5)
