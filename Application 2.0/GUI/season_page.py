import os
from tkinter import simpledialog, messagebox, filedialog
from classes.data_manager import DataManager
from classes.club import Club
from classes.player import Player
from classes.staff import Staff
from classes.team import Team


class SeasonPage:
    def __init__(self, gui_manager):
        """
        Initialise la gestion de la page Saison.

        Args:
            gui_manager (GUIManager): Instance de la classe GUIManager pour accéder aux données et méthodes de l'application.
        """
        self.gui_manager = gui_manager

    def archive_season(self):
        """
        Archive les données de la saison en cours en les sauvegardant dans un dossier nommé par l'utilisateur.
        """
        # Demander à l'utilisateur de nommer le dossier de la saison
        season_name = simpledialog.askstring("Nom de la saison", "Entrez le nom de la saison (par ex. Saison 2023):")
        if season_name:
            archive_folder = os.path.join(self.gui_manager.archives_folder, season_name)
            if not os.path.exists(archive_folder):
                os.makedirs(archive_folder)

                # Définir les chemins des fichiers source
                source_files = {
                    'club.json': os.path.join(self.gui_manager.data_folder, 'club.json'),
                    'players.json': os.path.join(self.gui_manager.data_folder, 'players.json'),
                    'staff.json': os.path.join(self.gui_manager.data_folder, 'staff.json'),
                    'teams.json': os.path.join(self.gui_manager.data_folder, 'teams.json'),
                    'matches.json': os.path.join(self.gui_manager.data_folder, 'matches.json'),
                    'trainings.json': os.path.join(self.gui_manager.data_folder, 'trainings.json')
                }

                # Archiver les fichiers existants dans le dossier de la saison
                for filename, filepath in source_files.items():
                    if os.path.exists(filepath):
                        DataManager.save_to_file(DataManager.load_from_file(filepath), os.path.join(archive_folder, filename))

                # Réinitialiser les données des evenements
                self.gui_manager.matches = []
                self.gui_manager.trainings = []

                # Sauvegarder les fichiers réinitialisés
                DataManager.save_to_file(self.gui_manager.matches, source_files['matches.json'])
                DataManager.save_to_file(self.gui_manager.trainings, source_files['trainings.json'])
                DataManager.save_to_file([player.to_dict() for player in self.gui_manager.players], source_files['players.json'])

                # Supprimer les fichiers JSON événements
                if os.path.exists(source_files['matches.json']):
                    os.remove(source_files['matches.json'])
                if os.path.exists(source_files['trainings.json']):
                    os.remove(source_files['trainings.json'])

                # Mettre à jour l'interface utilisateur avec les nouvelles données
                self.gui_manager.update_players_treeview()
                self.gui_manager.update_teams_treeview()

                messagebox.showinfo("Succès", f"La saison {season_name} a été archivée avec succès.")
            else:
                messagebox.showerror("Erreur", f"Le dossier {season_name} existe déjà.")

    def load_season(self):
        """
        Charge les données d'une saison archivée à partir d'un dossier sélectionné par l'utilisateur.
        """
        # Demander à l'utilisateur de sélectionner un dossier de saison
        archive_folder = filedialog.askdirectory(title="Sélectionnez le dossier de la saison à charger", initialdir=self.gui_manager.archives_folder)
        if archive_folder:
            try:
                # Définir les chemins des fichiers à charger
                archive_files = {
                    'club.json': os.path.join(archive_folder, 'club.json'),
                    'players.json': os.path.join(archive_folder, 'players.json'),
                    'staff.json': os.path.join(archive_folder, 'staff.json'),
                    'teams.json': os.path.join(archive_folder, 'teams.json'),
                    'matches.json': os.path.join(archive_folder, 'matches.json'),
                    'trainings.json': os.path.join(archive_folder, 'trainings.json')
                }

                # Chemins de destination dans le dossier data
                destination_files = {
                    'club.json': os.path.join(self.gui_manager.data_folder, 'club.json'),
                    'players.json': os.path.join(self.gui_manager.data_folder, 'players.json'),
                    'staff.json': os.path.join(self.gui_manager.data_folder, 'staff.json'),
                    'teams.json': os.path.join(self.gui_manager.data_folder, 'teams.json'),
                    'matches.json': os.path.join(self.gui_manager.data_folder, 'matches.json'),
                    'trainings.json': os.path.join(self.gui_manager.data_folder, 'trainings.json')
                }

                # Charger les données depuis l'archive et les sauvegarder dans le dossier data
                for filename, filepath in archive_files.items():
                    if os.path.exists(filepath):
                        data = DataManager.load_from_file(filepath)
                        DataManager.save_to_file(data, destination_files[filename])

                # Charger les données du club à partir du dossier sélectionné
                if os.path.exists(archive_files['club.json']):
                    club_data = DataManager.load_from_file(archive_files['club.json'])
                    if club_data is not None:
                        self.gui_manager.club = Club.from_dict(club_data)
                        self.gui_manager.update_club_info()  

                if os.path.exists(archive_files['players.json']):
                    players_data = DataManager.load_from_file(archive_files['players.json'])
                    if players_data is not None:
                        self.gui_manager.players = [Player.from_dict(data) for data in players_data]

                if os.path.exists(archive_files['staff.json']):
                    staff_data = DataManager.load_from_file(archive_files['staff.json'])
                    if staff_data is not None:
                        self.gui_manager.staff_members = [Staff.from_dict(data) for data in staff_data]

                if os.path.exists(archive_files['teams.json']):
                    teams_data = DataManager.load_from_file(archive_files['teams.json'])
                    if teams_data is not None:
                        self.gui_manager.teams = [Team.from_dict(data) for data in teams_data]

                if os.path.exists(archive_files['matches.json']):
                    matches_data = DataManager.load_from_file(archive_files['matches.json'])
                    if matches_data is not None:
                        self.gui_manager.matches = matches_data

                if os.path.exists(archive_files['trainings.json']):
                    trainings_data = DataManager.load_from_file(archive_files['trainings.json'])
                    if trainings_data is not None:
                        self.gui_manager.trainings = trainings_data

                # Mettre à jour l'interface utilisateur avec les nouvelles données
                self.gui_manager.update_players_treeview()
                self.gui_manager.update_staff_treeview()
                self.gui_manager.update_teams_treeview()

                messagebox.showinfo("Succès", f"La saison a été chargée avec succès depuis {archive_folder}.")
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors du chargement de la saison : {e}")
                print(f"Erreur lors du chargement de la saison : {e}")  
