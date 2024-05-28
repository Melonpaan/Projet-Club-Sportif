import tkinter as tk
from tkinter import ttk, messagebox
from classes.player import Player
from classes.staff import Staff
from GUI.player_page import PlayerPage

class GUIManager(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestion du club")
        self.geometry("800x600")

        self.joueurs = Player.load_from_file() 
        self.staff_members = Staff.load_from_file()

        # Boutons d'accueil, joueurs et staff
        self.button_frame = tk.Frame(self)
        self.button_frame.pack(side=tk.TOP, fill=tk.X)

        self.btn_accueil = tk.Button(self.button_frame, text="Accueil", command=self.show_accueil)
        self.btn_accueil.pack(side=tk.LEFT, padx=5, pady=5)

        self.btn_joueurs = tk.Button(self.button_frame, text="Joueurs", command=self.show_joueurs)
        self.btn_joueurs.pack(side=tk.LEFT, padx=5, pady=5)

        self.btn_staff = tk.Button(self.button_frame, text="Staff", command=self.show_staff)
        self.btn_staff.pack(side=tk.LEFT, padx=5, pady=5)

        # Frame pour les Treeviews
        self.tree_frame = tk.Frame(self)
        self.tree_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Treeview pour les joueurs
        self.tree_joueurs = ttk.Treeview(self.tree_frame, columns=(
            "ID", "Nom", "Prénom", "Date de Naissance", "Salaire", 
            "Contrat", "Adresse", "Téléphone", "Poste", "Numéro de Maillot"
        ), show='headings')
        self.tree_joueurs.heading("ID", text="ID")
        self.tree_joueurs.heading("Nom", text="Nom")
        self.tree_joueurs.heading("Prénom", text="Prénom")
        self.tree_joueurs.heading("Date de Naissance", text="Date de Naissance")
        self.tree_joueurs.heading("Salaire", text="Salaire")
        self.tree_joueurs.heading("Contrat", text="Contrat")
        self.tree_joueurs.heading("Adresse", text="Adresse")
        self.tree_joueurs.heading("Téléphone", text="Téléphone")
        self.tree_joueurs.heading("Poste", text="Poste")
        self.tree_joueurs.heading("Numéro de Maillot", text="Numéro de Maillot")
        self.tree_joueurs.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Treeview pour le staff
        self.tree_staff = ttk.Treeview(self.tree_frame, columns=("ID", "Nom", "Prénom", "Rôle"), show='headings')
        self.tree_staff.heading("ID", text="ID")
        self.tree_staff.heading("Nom", text="Nom")
        self.tree_staff.heading("Prénom", text="Prénom")
        self.tree_staff.heading("Rôle", text="Rôle")
        self.tree_staff.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Frames pour les boutons d'actions spécifiques
        self.joueur_action_frame = tk.Frame(self)
        self.staff_action_frame = tk.Frame(self)

        self.btn_ajouter_joueur = tk.Button(self.joueur_action_frame, text="Ajouter Joueur", command=lambda: PlayerPage.add_joueur(self))
        self.btn_ajouter_joueur.pack(side=tk.LEFT, padx=5, pady=5)

        self.btn_modifier_joueur = tk.Button(self.joueur_action_frame, text="Modifier Joueur", command=lambda: PlayerPage.modify_joueur(self))
        self.btn_modifier_joueur.pack(side=tk.LEFT, padx=5, pady=5)

        self.btn_supprimer_joueur = tk.Button(self.joueur_action_frame, text="Supprimer Joueur", command=lambda: PlayerPage.delete_joueur(self))
        self.btn_supprimer_joueur.pack(side=tk.LEFT, padx=5, pady=5)

        self.btn_ajouter_staff = tk.Button(self.staff_action_frame, text="Ajouter Staff", command=lambda: Staff.add_staff(self))
        self.btn_ajouter_staff.pack(side=tk.LEFT, padx=5, pady=5)

        self.btn_modifier_staff = tk.Button(self.staff_action_frame, text="Modifier Staff", command=lambda: Staff.modify_staff(self))
        self.btn_modifier_staff.pack(side=tk.LEFT, padx=5, pady=5)

        self.btn_supprimer_staff = tk.Button(self.staff_action_frame, text="Supprimer Staff", command=lambda: Staff.delete_staff(self))
        self.btn_supprimer_staff.pack(side=tk.LEFT, padx=5, pady=5)

        self.show_accueil()

    def show_accueil(self):
        self.clear_treeviews()
        self.clear_action_frames()
        messagebox.showinfo("Accueil", "Bienvenue dans l'application de gestion de l'équipe.")

    def show_joueurs(self):
        self.clear_treeviews()
        self.clear_action_frames()
        self.tree_joueurs.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.joueur_action_frame.pack(side=tk.BOTTOM, fill=tk.X)
        self.update_joueurs_treeview()

    def show_staff(self):
        self.clear_treeviews()
        self.clear_action_frames()
        self.tree_staff.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.staff_action_frame.pack(side=tk.BOTTOM, fill=tk.X)
        self.update_staff_treeview()

    def clear_treeviews(self):
        self.tree_joueurs.pack_forget()
        self.tree_staff.pack_forget()

    def clear_action_frames(self):
        self.joueur_action_frame.pack_forget()
        self.staff_action_frame.pack_forget()

    def update_joueurs_treeview(self):
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
        for item in self.tree_staff.get_children():
            self.tree_staff.delete(item)
        for staff in self.staff_members:
            self.tree_staff.insert("", "end", values=(
                staff.person_ID, staff.last_name, staff.first_name, 
                staff.role
            ))

