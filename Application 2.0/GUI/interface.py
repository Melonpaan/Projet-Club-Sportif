import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from classes.player import Player
from classes.staff import Staff
from classes.club import Club
from GUI.player_page import PlayerPage
from GUI.staff_page import StaffPage
from GUI.season_page import SeasonPage
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
        self.title("Gestion du club")
        self.geometry("800x600")

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
        self.load_initial_data()  # Charger les données initiales depuis le dossier data

        # Créer un Notebook pour les onglets
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Créer les frames pour chaque onglet
        self.accueil_frame = tk.Frame(self.notebook)
        self.player_frame = tk.Frame(self.notebook)
        self.staff_frame = tk.Frame(self.notebook)
        self.saison_frame = tk.Frame(self.notebook)

        # Ajouter les frames au Notebook
        self.notebook.add(self.accueil_frame, text="Accueil")
        self.notebook.add(self.player_frame, text="Joueurs")
        self.notebook.add(self.staff_frame, text="Staff")
        self.notebook.add(self.saison_frame, text="Saison")

        # Créer le contenu des frames
        self.create_accueil_frame(self.accueil_frame)
        self.create_player_frame(self.player_frame)
        self.create_staff_frame(self.staff_frame)
        self.create_saison_frame(self.saison_frame)

        # Charger les données initiales dans les Treeviews
        self.update_players_treeview()
        self.update_staff_treeview()
        self.update_club_info()

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

        players_data = DataManager.load_from_file(
            os.path.join(self.data_folder, 'players.json'))
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
            accueil_frame, f"Nombre d'équipes: 0", 6, 0)  # Initialement 0
        self.label_num_matches = Tools.create_label(
            accueil_frame, f"Nombre de matchs: 0", 7, 0)  # Initialement 0

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
            "Début Contrat", "Fin Contrat", "Adresse", "Téléphone", "Numéro de Maillot"
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
            "Début Contrat", "Fin Contrat", "Adresse", "Téléphone", "Rôle"
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
                player.address, player.phone_number, player.jersey_number
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
                staff.address, staff.phone_number, staff.role
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
        self.label_num_players.config(text=f"Nombre de joueurs: {len(
            self.players)}")
        # Mettre à jour le nombre de staff
        self.label_num_staff.config(text=f"Nombre de staff: {
                                    len(self.staff_members)}")
        # Mettre à jour le nombre d'équipes (initialement 0)
        self.label_num_teams.config(text=f"Nombre d'équipes: 0")
        # Mettre à jour le nombre de matchs (initialement 0)
        self.label_num_matches.config(text=f"Nombre de matchs: 0")

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
