import os
from tkinter import simpledialog, messagebox, filedialog
from tools import Tools
from classes.data_manager import DataManager
from classes.club import Club
from classes.player import Player
from classes.staff import Staff

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

                # Archiver les fichiers existants dans le dossier de la saison
                if os.path.exists(source_club_file):
                    DataManager.save_to_file(self.gui_manager.club.to_dict(), os.path.join(archive_folder, 'club.json'))
                if os.path.exists(source_players_file):
                    DataManager.save_to_file([player.to_dict() for player in self.gui_manager.players], os.path.join(archive_folder, 'players.json'))
                if os.path.exists(source_staff_file):
                    DataManager.save_to_file([staff.to_dict() for staff in self.gui_manager.staff_members], os.path.join(archive_folder, 'staff.json'))

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
                # Charger les données du club à partir du dossier sélectionné
                club_file = os.path.join(archive_folder, 'club.json')
                if os.path.exists(club_file):
                    club_data = DataManager.load_from_file(club_file)
                    if club_data is not None:
                        self.gui_manager.club = Club.from_dict(club_data)
                        self.gui_manager.update_club_info()  # Mettre à jour les informations du club dans l'interface

                # Charger les données des joueurs à partir du dossier sélectionné
                players_file = os.path.join(archive_folder, 'players.json')
                if os.path.exists(players_file):
                    players_data = DataManager.load_from_file(players_file)
                    if players_data is not None:
                        self.gui_manager.players = [Player.from_dict(data) for data in players_data]

                # Charger les données du staff à partir du dossier sélectionné
                staff_file = os.path.join(archive_folder, 'staff.json')
                if os.path.exists(staff_file):
                    staff_data = DataManager.load_from_file(staff_file)
                    if staff_data is not None:
                        self.gui_manager.staff_members = [Staff.from_dict(data) for data in staff_data]

                # Mettre à jour l'interface utilisateur avec les nouvelles données
                self.gui_manager.update_players_treeview()
                self.gui_manager.update_staff_treeview()

                messagebox.showinfo("Succès", f"La saison a été chargée avec succès depuis {archive_folder}.")
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors du chargement de la saison : {e}")
                print(f"Erreur lors du chargement de la saison : {e}")  # Débogage


