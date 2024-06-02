import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from classes.player import Player
from classes.staff import Staff
from classes.club import Club
from GUI.player_page import PlayerPage
from GUI.staff_page import StaffPage
from utils import Utils

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

        # Charger les données
        self.club = Club.load_from_file()
        self.joueurs = Player.load_from_file()
        self.staff_members = Staff.load_from_file()

        # Créer un Notebook pour les onglets
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Créer les frames pour chaque onglet
        self.accueil_frame = tk.Frame(self.notebook)
        self.joueur_frame = tk.Frame(self.notebook)
        self.staff_frame = tk.Frame(self.notebook)

        # Ajouter les frames au Notebook
        self.notebook.add(self.accueil_frame, text="Accueil")
        self.notebook.add(self.joueur_frame, text="Joueurs")
        self.notebook.add(self.staff_frame, text="Staff")

        # Créer le contenu des frames
        self.create_accueil_frame(self.accueil_frame)
        self.create_joueur_frame(self.joueur_frame)
        self.create_staff_frame(self.staff_frame)

        # Charger les données initiales dans les Treeviews
        self.update_joueurs_treeview()
        self.update_staff_treeview()

    def create_accueil_frame(self, frame):
        """
        Crée la frame pour l'accueil du club avec les informations du club et les boutons pour ajouter et supprimer des équipes.

        Args:
            frame (tk.Frame): Frame dans laquelle créer les widgets de l'accueil.
        """
        accueil_frame = tk.Frame(frame)
        accueil_frame.pack(expand=True)

        # Labels et entrées pour les informations du club
        self.entry_club_name = Utils.create_label_and_entry(accueil_frame, "Nom du Club:", 0, self.club.name)
        self.entry_club_address = Utils.create_label_and_entry(accueil_frame, "Adresse du Club:", 1, self.club.address)
        self.entry_club_president = Utils.create_label_and_entry(accueil_frame, "Président du Club:", 2, self.club.president)

        # Bouton pour sauvegarder les informations du club
        Utils.create_button(accueil_frame, "Sauvegarder", self.save_club_info, 3, 0, 2)

        # Listbox pour afficher les équipes
        self.team_listbox = tk.Listbox(accueil_frame, height=10, width=50)
        self.team_listbox.grid(row=4, column=0, columnspan=2, pady=10, sticky=tk.W + tk.E)
        self.update_team_listbox()

        # Boutons pour ajouter et supprimer des équipes
        Utils.create_button(accueil_frame, "Ajouter Équipe", self.add_team, 5, 0)
        Utils.create_button(accueil_frame, "Supprimer Équipe", self.remove_team, 5, 1)

    def create_joueur_frame(self, frame):
        """
        Crée la frame pour la gestion des joueurs avec les Treeviews et les boutons pour ajouter, modifier et supprimer des joueurs.

        Args:
            frame (tk.Frame): Frame dans laquelle créer les widgets pour les joueurs.
        """
        joueur_action_frame = tk.Frame(frame)
        joueur_action_frame.pack(side=tk.BOTTOM, fill=tk.X)

        # Treeview pour afficher les joueurs
        self.tree_joueurs = ttk.Treeview(frame, columns=(
            "ID", "Nom", "Prénom", "Date de Naissance", "Salaire",
            "Contrat", "Adresse", "Téléphone", "Poste", "Numéro de Maillot"
        ), show='headings')
        self.tree_joueurs.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Définir les en-têtes des colonnes du Treeview
        for col in self.tree_joueurs['columns']:
            self.tree_joueurs.heading(col, text=col)

        # Boutons pour gérer les joueurs
        self.player_page = PlayerPage(self)
        Utils.create_button(joueur_action_frame, "Ajouter Joueur", self.player_page.add_joueur, 0, 0)
        Utils.create_button(joueur_action_frame, "Modifier Joueur", self.player_page.modify_joueur, 0, 1)
        Utils.create_button(joueur_action_frame, "Supprimer Joueur", self.player_page.delete_joueur, 0, 2)

    def create_staff_frame(self, frame):
        """
        Crée la frame pour la gestion du staff avec les Treeviews et les boutons pour ajouter, modifier et supprimer du staff.

        Args:
            frame (tk.Frame): Frame dans laquelle créer les widgets pour le staff.
        """
        staff_action_frame = tk.Frame(frame)
        staff_action_frame.pack(side=tk.BOTTOM, fill=tk.X)

        # Treeview pour afficher le staff
        self.tree_staff = ttk.Treeview(frame, columns=("ID", "Nom", "Prénom", "Rôle"), show='headings')
        self.tree_staff.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Définir les en-têtes des colonnes du Treeview
        for col in self.tree_staff['columns']:
            self.tree_staff.heading(col, text=col)

        # Boutons pour gérer le staff
        self.staff_page = StaffPage(self)
        Utils.create_button(staff_action_frame, "Ajouter Staff", self.staff_page.add_staff, 0, 0)
        Utils.create_button(staff_action_frame, "Modifier Staff", self.staff_page.modify_staff, 0, 1)
        Utils.create_button(staff_action_frame, "Supprimer Staff", self.staff_page.delete_staff, 0, 2)

    def save_club_info(self):
        """
        Sauvegarde les informations du club à partir des entrées dans un fichier JSON.
        """
        self.club.name = self.entry_club_name.get()
        self.club.address = self.entry_club_address.get()
        self.club.president = self.entry_club_president.get()
        self.club.save_to_file()
        messagebox.showinfo("Information", "Informations du club sauvegardées.")

    def add_team(self):
        """
        Ajoute une nouvelle équipe au club et met à jour la listbox.
        """
        team_name = simpledialog.askstring("Ajouter Équipe", "Nom de l'équipe:")
        if team_name:
            self.club.add_team(team_name)
            self.update_team_listbox()
            messagebox.showinfo("Information", f"Équipe '{team_name}' ajoutée.")

    def remove_team(self):
        """
        Supprime l'équipe sélectionnée de la listbox et du club.
        """
        selected_team = self.team_listbox.get(tk.ACTIVE)
        if selected_team:
            self.club.remove_team(selected_team)
            self.update_team_listbox()
            messagebox.showinfo("Information", f"Équipe '{selected_team}' supprimée.")
        else:
            messagebox.showerror("Erreur", "Aucune équipe sélectionnée.")

    def update_team_listbox(self):
        """
        Met à jour la listbox avec les équipes actuelles du club.
        """
        self.team_listbox.delete(0, tk.END)
        for team in self.club.teams:
            self.team_listbox.insert(tk.END, team)

    def update_joueurs_treeview(self):
        """
        Met à jour le Treeview des joueurs avec les données actuelles.
        """
        for item in self.tree_joueurs.get_children():
            self.tree_joueurs.delete(item)
        for joueur in self.joueurs:
            self.tree_joueurs.insert("", "end", values=(
                joueur.person_ID, joueur.last_name, joueur.first_name,
                joueur.birth_date, joueur.salary, joueur.contract,
                joueur.address, joueur.phone_number, joueur.position,
                joueur.jersey_number
            ))

    def update_staff_treeview(self):
        """
        Met à jour le Treeview du staff avec les données actuelles.
        """
        for item in self.tree_staff.get_children():
            self.tree_staff.delete(item)
        for staff in self.staff_members:
            self.tree_staff.insert("", "end", values=(
                staff.person_ID, staff.last_name, staff.first_name,
                staff.role
            ))


































