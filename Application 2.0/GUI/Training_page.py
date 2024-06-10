from tkinter import Frame, Label, Button, Toplevel, Listbox, messagebox
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
        self.label = Label(self, text="Page des entrainements")
        self.label.grid(row=0, column=0, padx=10, pady=10)

        Tools.create_button(self, "Ajouter un entrainement", self.open_add_training_form, 1, 0)
        Tools.create_button(self, "Voir les entrainements", self.view_trainings, 2, 0)

    def open_add_training_form(self):
        """
        Ouvre une nouvelle fenêtre pour ajouter un nouvel entraînement.
        """
        self.add_training_window = Toplevel(self.master)
        self.add_training_window.title("Ajouter un entrainement")

        self.entry_date = Tools.create_label_and_entry(self.add_training_window, "Date (DD-MM-YYYY):", 0)
        self.entry_my_team = Tools.create_label_and_entry(self.add_training_window, "Mon équipe:", 1)
        self.entry_location = Tools.create_label_and_entry(self.add_training_window, "Lieu:", 2)

        Label(self.add_training_window, text="Joueurs:").grid(row=3, column=0, padx=10, pady=10)
        self.players_listbox = Listbox(self.add_training_window, selectmode="multiple")
        self.players_listbox.grid(row=3, column=1, padx=10, pady=10)
        self.populate_players_listbox()

        Button(self.add_training_window, text="Soumettre", command=self.add_training).grid(row=4, column=0, columnspan=2, pady=10)

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

    def add_training(self):
        """
        Ajoute un nouvel entraînement aux données des entraînements après validation des champs et de la date.
        """
        date = self.entry_date.get()
        my_team = self.entry_my_team.get()
        location = self.entry_location.get()
        selected_players = [self.players_listbox.get(i) for i in self.players_listbox.curselection()]

        if not date or not my_team or not location or not selected_players:
            messagebox.showerror("Erreur", "Tous les champs doivent être remplis.")
            return

        if not self.validate_date(date):
            messagebox.showerror("Erreur", "La date doit être au format DD-MM-YYYY.")
            return

        new_training = Training(date, my_team, location, selected_players)
        training_data = {
            "date": date,
            "my_team": my_team,
            "location": location,
            "players": selected_players
        }

        try:
            new_training.add_training(training_data)
            self.add_training_window.destroy()
        except FileNotFoundError as e:
            messagebox.showerror("Erreur", str(e))

    def view_trainings(self):
        """
        Ouvre une nouvelle fenêtre pour afficher tous les entraînements.
        """
        self.view_trainings_window = Toplevel(self.master)
        self.view_trainings_window.title("Voir les entrainements")

        trainings_data = DataManager.load_from_file('data/trainings.json')
        if trainings_data is not None:
            for index, training in enumerate(trainings_data):
                Label(self.view_trainings_window, text=f"{training['my_team']} vs {training['location']} - {training['date']}").grid(row=index, column=0, padx=10, pady=5)
                Button(self.view_trainings_window, text="Voir plus", command=lambda m=training: self.view_training_details(m)).grid(row=index, column=1, padx=10, pady=5)

    def view_training_details(self, training):
        """
        Ouvre une nouvelle fenêtre pour afficher les détails d'un entraînement spécifique.

        Args:
            training (dict): Les données de l'entraînement à afficher.
        """
        details_window = Toplevel(self.master)
        details_window.title("Détails de l'entrainement")

        Label(details_window, text=f"Date : {training['date']}").pack(padx=10, pady=5)
        Label(details_window, text=f"Mon équipe : {training['my_team']}").pack(padx=10, pady=5)
        Label(details_window, text=f"Lieu : {training['location']}").pack(padx=10, pady=5)
        Label(details_window, text=f"Joueurs : {', '.join(training['players'])}").pack(padx=10, pady=5)
        Label(details_window, text=f"Type d'entraînement : ").pack(padx=10, pady=5)
