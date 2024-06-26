import tkinter as tk
from tkinter import ttk, messagebox
from classes.player import Player
from classes.staff import Staff
from classes.club import Club
from classes.team import Team
from GUI.player_page import PlayerPage
from GUI.staff_page import StaffPage
from GUI.season_page import SeasonPage
from GUI.team_page import TeamPage
from GUI.Match_page import MatchPage
from GUI.Training_page import TrainingPage
from GUI.Statistics_page import StatisticsPage
from classes.Match import Match
from classes.Training import Training
from tools import Tools
from classes.data_manager import DataManager
import os

class GUIManager(tk.Tk):
    """
    Classe principale pour gérer l'interface utilisateur de l'application de gestion du club.
    Hérite de tk.Tk pour créer une fenêtre principale Tkinter.
    """

    def __init__(self):
        """
        Initialise la fenêtre principale et crée les frames pour l'interface du club et les autres sections.
        Charge les données du club, des joueurs et du staff à partir de fichiers.
        """
        super().__init__()
        self.title("Gestion de club de foot")
        self.geometry("950x750")

        # Définir le dossier de données et d'archives relatif au script principal
        self.base_dir = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..'))
        self.data_folder = os.path.join(self.base_dir, 'data')
        self.archives_folder = os.path.join(self.base_dir, 'archives')

        # Créer les dossiers s'ils n'existent pas
        if not os.path.exists(self.data_folder):
            os.makedirs(self.data_folder)
        if not os.path.exists(self.archives_folder):
            os.makedirs(self.archives_folder)

        # Charger les données
        self.load_initial_data()  

        # Créer un Notebook pour les onglets
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Créer les frames pour chaque onglet
        self.accueil_frame = tk.Frame(self.notebook)
        self.player_frame = tk.Frame(self.notebook)
        self.staff_frame = tk.Frame(self.notebook)
        self.saison_frame = tk.Frame(self.notebook)
        self.team_frame = tk.Frame(self.notebook)
        self.events_frame = tk.Frame(self.notebook)
        self.statistics_frame = tk.Frame(self.notebook) 

        # Ajouter les frames au Notebook
        self.notebook.add(self.accueil_frame, text="Accueil")
        self.notebook.add(self.player_frame, text="Joueurs")
        self.notebook.add(self.staff_frame, text="Staff")
        self.notebook.add(self.team_frame, text="Equipe")
        self.notebook.add(self.events_frame, text="Evenements")
        self.notebook.add(self.statistics_frame, text="Statistiques")  
        self.notebook.add(self.saison_frame, text="Saison")

        # Créer le contenu des frames
        self.create_accueil_frame(self.accueil_frame)
        self.create_player_frame(self.player_frame)
        self.create_staff_frame(self.staff_frame)
        self.create_team_frame(self.team_frame)
        self.create_saison_frame(self.saison_frame)
        self.create_events_frame(self.events_frame)
        self.create_statistics_frame(self.statistics_frame)  

        # Charger les données initiales dans les Treeviews
        self.update_players_treeview()
        self.update_staff_treeview()
        self.update_club_info()
        self.update_teams_treeview()

    def load_initial_data(self):
        """
        Charge les données initiales depuis le dossier data.
        """
        club_data = DataManager.load_from_file(
            os.path.join(self.data_folder, 'club.json'))
        if club_data is not None:
            self.club = Club.from_dict(club_data)
        else:
            self.club = Club("Nom du Club", "Adresse du Club",
                             "Président du Club")
    
        players_data = DataManager.load_from_file(os.path.join(self.data_folder, 'players.json'))
        if players_data is not None:
            self.players = [Player.from_dict(data) for data in players_data]
        else:
            self.players = []
    
        staff_data = DataManager.load_from_file(
            os.path.join(self.data_folder, 'staff.json'))
        if staff_data is not None:
            self.staff_members = [Staff.from_dict(data) for data in staff_data]
        else:
            self.staff_members = []

        teams_data = DataManager.load_from_file(
            os.path.join(self.data_folder,'teams.json'))
        if teams_data is not None:
            self.teams = [Team.from_dict(data)for data in teams_data]
        else:
            self.teams = []

        matches_data = DataManager.load_from_file(os.path.join(self.data_folder, 'matches.json'))
        if matches_data is not None:
            self.matches = [Match.from_dict(data) for data in matches_data]  
        else:
            self.matches = []

        trainings_data = DataManager.load_from_file(os.path.join(self.data_folder, 'trainings.json'))
        if trainings_data is not None:
            self.trainings = [Training.from_dict(data) for data in trainings_data]  
        else:
            self.trainings = []

    def create_accueil_frame(self, frame):
        """
        Crée la frame pour l'accueil du club avec les informations du club et les boutons pour ajouter et supprimer des équipes.

        Args:
            frame (tk.Frame): Frame dans laquelle créer les widgets de l'accueil.
        """
        accueil_frame = tk.Frame(frame)
        accueil_frame.pack(expand=True)

        # Labels et entrées pour les informations du club
        self.entry_club_name = Tools.create_label_and_entry(
            accueil_frame, "Nom du Club:", 0, self.club.name)
        self.entry_club_address = Tools.create_label_and_entry(
            accueil_frame, "Adresse du Club:", 1, self.club.address)
        self.entry_club_president = Tools.create_label_and_entry(
            accueil_frame, "Président du Club:", 2, self.club.president)

        # Bouton pour sauvegarder les informations du club
        Tools.create_button(accueil_frame, "Sauvegarder",
                            self.save_club_info, 3, 0, 2)

        # Labels pour afficher les informations clés
        self.label_num_players = Tools.create_label(
            accueil_frame, f"Nombre de joueurs: {len(self.players)}", 4, 0)
        self.label_num_staff = Tools.create_label(
            accueil_frame, f"Nombre de staff: {len(self.staff_members)}", 5, 0)
        self.label_num_teams = Tools.create_label(
            accueil_frame, f"Nombre d'équipes: {len(self.teams)}", 6, 0)
        self.label_num_matches = Tools.create_label(
            accueil_frame, f"Nombre de matchs: {len(self.matches)}", 7, 0)
        self.label_num_trainings = Tools.create_label(
            accueil_frame, f"Nombre d'entraînements: {len(self.trainings)}", 8, 0)
        self.label_total_player_salary = Tools.create_label(
            accueil_frame, f"Total salaire des joueurs: {self.calculate_total_salary(self.players)} €", 9, 0)
        self.label_total_staff_salary = Tools.create_label(
            accueil_frame, f"Total salaire du staff: {self.calculate_total_salary(self.staff_members)} €", 10, 0)


    def calculate_total_salary(self, members):
        """
        Calcule le total des salaires des membres donnés.

        Args:
            members (list): Liste des membres (joueurs ou staff).

        Returns:
            int: Total des salaires.
        """
        total_salary = 0
        for member in members:
            try:
                total_salary += int(member.contract.salary)
            except (ValueError, TypeError):
                continue
        return total_salary

    def create_player_frame(self, frame):
        """
        Crée la frame pour la gestion des joueurs avec les Treeviews et les boutons pour ajouter, modifier et supprimer des joueurs.

        Args:
            frame (tk.Frame): Frame dans laquelle créer les widgets pour les joueurs.
        """
        player_action_frame = tk.Frame(frame)
        player_action_frame.pack(side=tk.BOTTOM, fill=tk.X)

        # Treeview pour afficher les joueurs
        self.tree_players = ttk.Treeview(frame, columns=(
            "ID", "Nom", "Prénom", "Poste", "Date de Naissance", "Salaire",
            "Début Contrat", "Fin Contrat", "Adresse", "Téléphone", "Numéro de Maillot", "Genre"
        ), show='headings')
        self.tree_players.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Définir les en-têtes des colonnes du Treeview
        for col in self.tree_players['columns']:
            self.tree_players.heading(col, text=col)

        # Boutons pour gérer les joueurs
        self.player_page = PlayerPage(self)
        Tools.create_button(player_action_frame, "Ajouter Joueur",
                            self.player_page.add_player, 0, 0)
        Tools.create_button(player_action_frame, "Modifier Joueur",
                            self.player_page.modify_player, 0, 1)
        Tools.create_button(player_action_frame, "Supprimer Joueur",
                            self.player_page.delete_player, 0, 2)

    def create_staff_frame(self, frame):
        """
        Crée la frame pour la gestion du staff avec les Treeviews et les boutons pour ajouter, modifier et supprimer du staff.

        Args:
            frame (tk.Frame): Frame dans laquelle créer les widgets pour le staff.
        """
        staff_action_frame = tk.Frame(frame)
        staff_action_frame.pack(side=tk.BOTTOM, fill=tk.X)

        # Treeview pour afficher le staff
        self.tree_staff = ttk.Treeview(frame, columns=(
            "ID", "Nom", "Prénom", "Date de Naissance", "Salaire",
            "Début Contrat", "Fin Contrat", "Adresse", "Téléphone", "Rôle", "Genre"
        ), show='headings')
        self.tree_staff.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Définir les en-têtes des colonnes du Treeview
        for col in self.tree_staff['columns']:
            self.tree_staff.heading(col, text=col)

        # Boutons pour gérer le staff
        self.staff_page = StaffPage(self)
        Tools.create_button(staff_action_frame, "Ajouter Staff",
                            self.staff_page.add_staff, 0, 0)
        Tools.create_button(staff_action_frame, "Modifier Staff",
                            self.staff_page.modify_staff, 0, 1)
        Tools.create_button(staff_action_frame, "Supprimer Staff",
                            self.staff_page.delete_staff, 0, 2)

    def save_club_info(self):
        """
        Sauvegarde les informations du club à partir des entrées dans un fichier JSON.
        """
        self.club.name = self.entry_club_name.get()
        self.club.address = self.entry_club_address.get()
        self.club.president = self.entry_club_president.get()
        self.club.save_to_file(os.path.join(self.data_folder, 'club.json'))
        messagebox.showinfo(
            "Information", "Informations du club sauvegardées.")
        # Mettre à jour les informations de l'accueil après la sauvegarde
        self.update_accueil_info()

    def update_players_treeview(self):
        """
        Met à jour le Treeview des joueurs avec les données actuelles.
        """
        for item in self.tree_players.get_children():
            self.tree_players.delete(item)
        for player in self.players:
            self.tree_players.insert("", "end", values=(
                player.person_ID, player.last_name, player.first_name, player.position,
                player.birth_date, player.contract.salary,
                player.contract.start_date, player.contract.end_date,
                player.address, player.phone_number, player.jersey_number, player.gender
            ))
        # Mettre à jour les informations de l'accueil après la mise à jour des joueurs
        self.update_accueil_info()

    def update_staff_treeview(self):
        """
        Met à jour le Treeview du staff avec les données actuelles.
        """
        for item in self.tree_staff.get_children():
            self.tree_staff.delete(item)
        for staff in self.staff_members:
            self.tree_staff.insert("", "end", values=(
                staff.person_ID, staff.last_name, staff.first_name,
                staff.birth_date, staff.contract.salary,
                staff.contract.start_date, staff.contract.end_date,
                staff.address, staff.phone_number, staff.role, staff.gender
            ))
        # Mettre à jour les informations de l'accueil après la mise à jour du staff
        self.update_accueil_info()

    def update_club_info(self):
        """
        Met à jour les informations du club dans l'interface utilisateur avec les données actuelles.
        """
        self.entry_club_name.delete(0, tk.END)
        self.entry_club_name.insert(0, self.club.name)
        self.entry_club_address.delete(0, tk.END)
        self.entry_club_address.insert(0, self.club.address)
        self.entry_club_president.delete(0, tk.END)
        self.entry_club_president.insert(0, self.club.president)
        # Mettre à jour les informations de l'accueil après la mise à jour du club
        self.update_accueil_info()

    def update_accueil_info(self):
        """
        Met à jour les informations de l'accueil (nombre de joueurs, nombre de staff, nombre d'équipes, nombre de matchs).
        """
        # Mettre à jour le nombre de joueurs
        self.label_num_players.config(text=f"Nombre de joueurs: {len(self.players)}")
        # Mettre à jour le nombre de staff
        self.label_num_staff.config(text=f"Nombre de staff: {len(self.staff_members)}")
        # Mettre à jour le nombre d'équipes (initialement 0)
        self.label_num_teams.config(text=f"Nombre d'équipes: {len(self.teams)}")
        # Mettre à jour le nombre de matchs (initialement 0)
        self.label_num_matches.config(text=f"Nombre de matchs: {len(self.matches)}")
        # Mettre à jour le nombre d'entraînements (initialement 0)
        self.label_num_trainings.config(text=f"Nombre d'entraînements: {len(self.trainings)}")
        # Mettre à jour le total des salaires des joueurs
        self.label_total_player_salary.config(text=f"Total salaire des joueurs: {self.calculate_total_salary(self.players)} €")
        # Mettre à jour le total des salaires du staff
        self.label_total_staff_salary.config(text=f"Total salaire du staff: {self.calculate_total_salary(self.staff_members)} €")

    def create_saison_frame(self, frame):
        """
        Crée la frame pour l'onglet Saison avec les boutons pour archiver et charger des saisons.

        Args:
            frame (tk.Frame): Frame dans laquelle créer les widgets de l'onglet Saison.
        """
        saison_frame = tk.Frame(frame)
        saison_frame.pack(expand=True)

        # Initialiser la gestion de la page Saison
        self.season_page = SeasonPage(self)

        # Bouton pour archiver la saison
        Tools.create_button(saison_frame, "Archiver la Saison",
                            self.season_page.archive_season, 0, 0)
        # Bouton pour charger une saison archivée
        Tools.create_button(saison_frame, "Charger une Saison",
                            self.season_page.load_season, 1, 0)

    def create_team_frame(self, frame):
        """
        Crée la frame pour la gestion des équipes avec les Treeviews et les boutons pour ajouter, modifier et supprimer des équipes.
        """
        team_action_frame = tk.Frame(frame)
        team_action_frame.pack(side=tk.BOTTOM, fill=tk.X)

        # Treeview pour afficher les équipes
        self.tree_teams = ttk.Treeview(frame, columns=(
            "ID", "Nom", "Genre", "Catégorie","Médecin", "Entraîneur"
        ), show='headings')
        self.tree_teams.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Définir les en-têtes des colonnes du Treeview
        for col in self.tree_teams['columns']:
            self.tree_teams.heading(col, text=col)

        # Boutons pour gérer les équipes
        self.team_page = TeamPage(self)
        Tools.create_button(team_action_frame, "Ajouter Équipe",
                            self.team_page.add_team, 0, 0)
        Tools.create_button(team_action_frame, "Modifier Équipe",
                            self.team_page.modify_team, 0, 1)
        Tools.create_button(team_action_frame, "Supprimer Équipe",
                            self.team_page.delete_team, 0, 2)
        Tools.create_button(team_action_frame, "Ajouter joueurs à l'Équipe",
                            self.team_page.add_players_to_team, 0,3)
        Tools.create_button(team_action_frame, "Voir Joueurs de l'Équipe",
                            self.team_page.view_team_players,0, 4)

    def update_teams_treeview(self):
        """
        Met à jour le Treeview des équipes avec les données actuelles.
        """
        for item in self.tree_teams.get_children():
            self.tree_teams.delete(item)

        for team in self.teams:
            doctor_name = self.get_staff_name_by_id(team.doctor_id)
            coach_name = self.get_staff_name_by_id(team.coach_id)
            self.tree_teams.insert("", "end", values=(
                team.team_id, team.name, team.gender, team.category, doctor_name, coach_name
            ))
        self.update_accueil_info()

    def get_staff_name_by_id(self, staff_id):
        """
        Retourne le nom complet du staff à partir de son ID.
        """
        if staff_id is None:
            return ""
        for staff in self.staff_members:
            if staff.person_ID == staff_id:
                return f"{staff.first_name} {staff.last_name}"
        return ""

    def create_events_frame(self, frame):
        """
        Crée la frame pour l'onglet Événements avec les sous-boutons Matchs et Entraînement.

        Args:
            frame (tk.Frame): Frame dans laquelle créer les widgets de l'onglet Événements.
        """
        events_frame = tk.Frame(frame)
        events_frame.pack(expand=True, fill=tk.BOTH)

        # Container for centering buttons
        button_container = tk.Frame(events_frame)
        button_container.pack(expand=True)

        # Boutons pour accéder aux pages Matchs et Entraînement
        match_button = tk.Button(button_container, text="Matchs", command=self.open_match_page,
                                 width=20, height=2)
        match_button.pack(pady=10)

        training_button = tk.Button(button_container, text="Entraînement", command=self.open_training_page,
                                    width=20, height=2)
        training_button.pack(pady=10)

    def open_match_page(self):
        """
        Ouvre la page de gestion des matchs avec un sous-bouton pour les statistiques du match.
        """
        match_page = tk.Toplevel(self)
        match_page.title("Matchs")
        match_frame = MatchPage(match_page)
        match_frame.pack(fill=tk.BOTH, expand=True)

    def open_training_page(self):
        """
        Ouvre la page de gestion des entraînements.
        """
        training_page = tk.Toplevel(self)
        training_page.title("Entraînements")
        training_frame = TrainingPage(training_page)
        training_frame.pack(fill=tk.BOTH, expand=True)

    def create_statistics_frame(self, frame):
        """
       Crée la frame pour l'onglet Statistiques avec les statistiques des joueurs.
       Args:
           frame (tk.Frame): Frame dans laquelle créer les widgets de l'onglet Statistiques.
       """
        statistics_page = StatisticsPage(frame)
        statistics_page.pack(fill=tk.BOTH, expand=True)

