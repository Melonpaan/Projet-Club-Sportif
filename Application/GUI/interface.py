import tkinter as tk
from tkinter import ttk, messagebox
from classes.player import Player
from classes.staff import Staff
from GUI.player_page import PlayerPage
from GUI.staff_page import StaffPage

class GUIManager(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestion du club")
        self.geometry("800x600")

        self.players = Player.load_from_file() 
        self.staff_members = Staff.load_from_file()

        # Boutons d'accueil, players et staff
        self.button_frame = tk.Frame(self)
        self.button_frame.pack(side=tk.TOP, fill=tk.X)

        self.btn_accueil = tk.Button(self.button_frame, text="Accueil", command=self.show_accueil)
        self.btn_accueil.pack(side=tk.LEFT, padx=5, pady=5)

        self.btn_players = tk.Button(self.button_frame, text="players", command=self.show_players)
        self.btn_players.pack(side=tk.LEFT, padx=5, pady=5)

        self.btn_staff = tk.Button(self.button_frame, text="Staff", command=self.show_staff)
        self.btn_staff.pack(side=tk.LEFT, padx=5, pady=5)

        # Frame pour les Treeviews
        self.tree_frame = tk.Frame(self)
        self.tree_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Treeview pour les players
        self.tree_players = ttk.Treeview(self.tree_frame, columns=(
            "ID", "Nom", "Prénom", "Date de Naissance", "Salaire", 
            "Contrat", "Adresse", "Téléphone", "Poste", "Numéro de Maillot"
        ), show='headings')
        self.tree_players.heading("ID", text="ID")
        self.tree_players.heading("Nom", text="Nom")
        self.tree_players.heading("Prénom", text="Prénom")
        self.tree_players.heading("Date de Naissance", text="Date de Naissance")
        self.tree_players.heading("Salaire", text="Salaire")
        self.tree_players.heading("Contrat", text="Contrat")
        self.tree_players.heading("Adresse", text="Adresse")
        self.tree_players.heading("Téléphone", text="Téléphone")
        self.tree_players.heading("Poste", text="Poste")
        self.tree_players.heading("Numéro de Maillot", text="Numéro de Maillot")
        self.tree_players.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Treeview pour le staff
        self.tree_staff = ttk.Treeview(self.tree_frame, columns=("ID", "Nom", "Prénom", "Rôle"), show='headings')
        self.tree_staff.heading("ID", text="ID")
        self.tree_staff.heading("Nom", text="Nom")
        self.tree_staff.heading("Prénom", text="Prénom")
        self.tree_staff.heading("Rôle", text="Rôle")
        self.tree_staff.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Frames pour les boutons d'actions spécifiques
        self.player_action_frame = tk.Frame(self)
        self.staff_action_frame = tk.Frame(self)

        self.player_page = PlayerPage(self)
        self.staff_page=StaffPage(self)

        self.btn_ajouter_player = tk.Button(self.player_action_frame, text="Ajouter player", command=self.player_page.add_player)
        self.btn_ajouter_player.pack(side=tk.LEFT, padx=5, pady=5)

        self.btn_modifier_player = tk.Button(self.player_action_frame, text="Modifier player", command=self.player_page.modify_player)
        self.btn_modifier_player.pack(side=tk.LEFT, padx=5, pady=5)

        self.btn_supprimer_player = tk.Button(self.player_action_frame, text="Supprimer player", command=self.player_page.delete_player)
        self.btn_supprimer_player.pack(side=tk.LEFT, padx=5, pady=5)

        self.btn_ajouter_staff = tk.Button(self.staff_action_frame, text="Ajouter Staff", command=self.staff_page.add_staff)
        self.btn_ajouter_staff.pack(side=tk.LEFT, padx=5, pady=5)

        self.btn_modifier_staff = tk.Button(self.staff_action_frame, text="Modifier Staff", command=self.staff_page.modify_staff)
        self.btn_modifier_staff.pack(side=tk.LEFT, padx=5, pady=5)

        self.btn_supprimer_staff = tk.Button(self.staff_action_frame, text="Supprimer Staff", command=self.staff_page.delete_staff)
        self.btn_supprimer_staff.pack(side=tk.LEFT, padx=5, pady=5)

        self.show_accueil()

    def show_accueil(self):
        self.clear_treeviews()
        self.clear_action_frames()
        messagebox.showinfo("Accueil", "Bienvenue dans l'application de gestion de l'équipe.")

    def show_players(self):
        self.clear_treeviews()
        self.clear_action_frames()
        self.tree_players.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.player_action_frame.pack(side=tk.BOTTOM, fill=tk.X)
        self.update_players_treeview()

    def show_staff(self):
        self.clear_treeviews()
        self.clear_action_frames()
        self.tree_staff.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.staff_action_frame.pack(side=tk.BOTTOM, fill=tk.X)
        self.update_staff_treeview()

    def clear_treeviews(self):
        self.tree_players.pack_forget()
        self.tree_staff.pack_forget()

    def clear_action_frames(self):
        self.player_action_frame.pack_forget()
        self.staff_action_frame.pack_forget()

    def update_players_treeview(self):
        for item in self.tree_players.get_children():
            self.tree_players.delete(item)
        for player in self.players:
            self.tree_players.insert("", "end", values=(
                player.person_ID, player.last_name, player.first_name, 
                player.birth_date, player.salary, player.contract, 
                player.address, player.phone_number, player.position, 
                player.jersey_number
            ))

    def update_staff_treeview(self):
        for item in self.tree_staff.get_children():
            self.tree_staff.delete(item)
        for staff in self.staff_members:
            self.tree_staff.insert("", "end", values=(
                staff.person_ID, staff.last_name, staff.first_name, 
                staff.role
            ))