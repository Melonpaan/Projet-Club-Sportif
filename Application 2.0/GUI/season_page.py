import os
from tkinter import simpledialog, messagebox, filedialog
from tools import Tools
from classes.data_manager import DataManager
from classes.club import Club
from classes.player import Player
from classes.staff import Staff
from classes.team import Team
from classes.Match import Match
from classes.Training import Training

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
                source_club_file = os.path.join(self.gui_manager.data_folder, 'club.json')
                source_players_file = os.path.join(self.gui_manager.data_folder, 'players.json')
                source_staff_file = os.path.join(self.gui_manager.data_folder, 'staff.json')
                source_teams_file = os.path.join(self.gui_manager.data_folder, 'teams.json')
                source_matches_file = os.path.join(self.gui_manager.data_folder, 'matches.json')
                source_trainings_file = os.path.join(self.gui_manager.data_folder, 'trainings.json')

                # Archiver les fichiers existants dans le dossier de la saison
                if os.path.exists(source_club_file):
                    DataManager.save_to_file(self.gui_manager.club.to_dict(), os.path.join(archive_folder, 'club.json'))
                if os.path.exists(source_players_file):
                    DataManager.save_to_file([player.to_dict() for player in self.gui_manager.players], os.path.join(archive_folder, 'players.json'))
                if os.path.exists(source_staff_file):
                    DataManager.save_to_file([staff.to_dict() for staff in self.gui_manager.staff_members], os.path.join(archive_folder, 'staff.json'))
                if os.path.exists(source_teams_file):
                    DataManager.save_to_file([team.to_dict() for team in self.gui_manager.teams], os.path.join(archive_folder, 'teams.json'))
                if os.path.exists(source_matches_file):
                    DataManager.save_to_file([match.to_dict() for match in self.gui_manager.matches], os.path.join(archive_folder, 'matches.json'))  # Archiver les matchs
                if os.path.exists(source_trainings_file):
                    DataManager.save_to_file([training.to_dict() for training in self.gui_manager.trainings], os.path.join(archive_folder, 'trainings.json'))  # Archiver les entraînements

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
                club_file = os.path.join(archive_folder, 'club.json')
                players_file = os.path.join(archive_folder, 'players.json')
                staff_file = os.path.join(archive_folder, 'staff.json')
                teams_file = os.path.join(archive_folder, 'teams.json')
                matches_file = os.path.join(archive_folder, 'matches.json')
                trainings_file = os.path.join(archive_folder, 'trainings.json')

                # Charger les données du club à partir du dossier sélectionné
                if os.path.exists(club_file):
                    club_data = DataManager.load_from_file(club_file)
                    if club_data is not None:
                        self.gui_manager.club = Club.from_dict(club_data)
                        self.gui_manager.update_club_info()  # Mettre à jour les informations du club dans l'interface

                # Charger les données des joueurs à partir du dossier sélectionné
                if os.path.exists(players_file):
                    players_data = DataManager.load_from_file(players_file)
                    if players_data is not None:
                        self.gui_manager.players = [Player.from_dict(data) for data in players_data]

                # Charger les données du staff à partir du dossier sélectionné
                if os.path.exists(staff_file):
                    staff_data = DataManager.load_from_file(staff_file)
                    if staff_data is not None:
                        self.gui_manager.staff_members = [Staff.from_dict(data) for data in staff_data]

                # Charger les données des équipes à partir du dossier sélectionné
                if os.path.exists(teams_file):
                    teams_data = DataManager.load_from_file(teams_file)
                    if teams_data is not None:
                        self.gui_manager.teams = [Team.from_dict(data) for data in teams_data]

                # Charger les données des matchs à partir du dossier sélectionné
                if os.path.exists(matches_file):
                    matches_data = DataManager.load_from_file(matches_file)
                    if matches_data is not None:
                        self.gui_manager.matches = [Match.from_dict(data) for data in matches_data]  # Charger les matchs

                # Charger les données des entraînements à partir du dossier sélectionné
                if os.path.exists(trainings_file):
                    trainings_data = DataManager.load_from_file(trainings_file)
                    if trainings_data is not None:
                        self.gui_manager.trainings = [Training.from_dict(data) for data in trainings_data]  # Charger les entraînements

                # Mettre à jour l'interface utilisateur avec les nouvelles données
                self.gui_manager.update_players_treeview()
                self.gui_manager.update_staff_treeview()
                self.gui_manager.update_teams_treeview()
                
                # Sauvegarder les données chargées dans les fichiers actifs
                #DataManager.save_to_file([match.to_dict() for match in self.gui_manager.matches], os.path.join(self.gui_manager.data_folder, 'matches.json'))
                #DataManager.save_to_file([training.to_dict() for training in self.gui_manager.trainings], os.path.join(self.gui_manager.data_folder, 'trainings.json'))

                messagebox.showinfo("Succès", f"La saison a été chargée avec succès depuis {archive_folder}.")
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors du chargement de la saison : {e}")
                print(f"Erreur lors du chargement de la saison : {e}")  # Débogage
