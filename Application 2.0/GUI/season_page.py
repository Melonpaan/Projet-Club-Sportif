# season_page.py

import os
from tkinter import simpledialog, messagebox, filedialog
from utils import Utils
from classes.data_manager import DataManager

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
            archive_folder = f"archives/{season_name}"
            if not os.path.exists(archive_folder):
                os.makedirs(archive_folder)

                # Copier les fichiers JSON existants dans le nouveau dossier de la saison
                DataManager.save_to_file(self.gui_manager.club.to_dict(), f"{archive_folder}/club.json")
                DataManager.save_to_file([player.to_dict() for player in self.gui_manager.players], f"{archive_folder}/players.json")
                DataManager.save_to_file([staff.to_dict() for staff in self.gui_manager.staff_members], f"{archive_folder}/staff.json")

                messagebox.showinfo("Succès", f"La saison {season_name} a été archivée avec succès.")
            else:
                messagebox.showerror("Erreur", f"Le dossier {season_name} existe déjà.")

    def load_season(self):
        """
        Charge les données d'une saison archivée à partir d'un dossier sélectionné par l'utilisateur.
        """
        # Demander à l'utilisateur de sélectionner un dossier de saison
        archive_folder = filedialog.askdirectory(title="Sélectionnez le dossier de la saison à charger", initialdir="archives")
        if archive_folder:
            try:
                # Charger les données du club à partir du dossier sélectionné
                club_data = DataManager.load_from_file(f"{archive_folder}/club.json")
                self.gui_manager.club = Club.from_dict(club_data)

                # Charger les données des joueurs à partir du dossier sélectionné
                players_data = DataManager.load_from_file(f"{archive_folder}/players.json")
                self.gui_manager.players = [Player.from_dict(data) for data in players_data]

                # Charger les données du staff à partir du dossier sélectionné
                staff_data = DataManager.load_from_file(f"{archive_folder}/staff.json")
                self.gui_manager.staff_members = [Staff.from_dict(data) for data in staff_data]

                # Mettre à jour l'interface utilisateur avec les nouvelles données
                self.gui_manager.update_players_treeview()
                self.gui_manager.update_staff_treeview()

                messagebox.showinfo("Succès", f"La saison a été chargée avec succès depuis {archive_folder}.")
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors du chargement de la saison : {e}")
