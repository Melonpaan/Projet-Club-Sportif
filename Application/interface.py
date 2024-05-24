import tkinter as tk
from joueur import Joueur


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Club de foot')
        self.geometry('1280x720')
        self.frames = {}
        self.joueurs = Joueur.charger_joueurs("Application/data/joueurs.json")

        self.sidebar = tk.Frame(self, width=320, bg='#2e2e2e', height=720, borderwidth=2)
        self.sidebar.pack(expand=False, fill='both', side='left')

        self.main_window = tk.Frame(self, bg='#cccccc', width=960, height=720)
        self.main_window.pack(expand=True, fill='both', side='right')

        self.main_window.grid_rowconfigure(0, weight=1)
        self.main_window.grid_columnconfigure(0, weight=1)

        self.add_sidebar_buttons()
        self.create_frame()

    def add_sidebar_buttons(self):
        Club_btn = tk.Button(self.sidebar, text='Club', command=lambda: self.show_frame("Club"))
        Club_btn.pack(fill='x')
        Player_btn = tk.Button(self.sidebar, text='Joueur', command=lambda: self.show_frame("Player"))
        Player_btn.pack(fill='x')
        Equipe_btn = tk.Button(self.sidebar, text='Equipe', command=lambda: self.show_frame("Equipe"))
        Equipe_btn.pack(fill='x')

    def create_frame(self):
        club_frame = tk.Frame(self.main_window, bg='red')
        player_frame = self.frame_joueur()
        equipe_frame = self.frame_equipe()

        frames_list = [club_frame, player_frame, equipe_frame]
        names = ['Club', 'Player', 'Equipe']

        for i in range(len(frames_list)):
            F = frames_list[i]
            name = names[i]
            self.frames[name] = F
            F.grid(row=0, column=0, sticky='nsew')
        self.show_frame("Player")

    def frame_joueur(self):
        frame = tk.Frame(self.main_window, bg='grey')

        labels = ["Nom", "Prénom", "Date de naissance (JJ/MM/AAAA)", "Poste", "Position", "Salaire (€)", "Contrat (Durée)"]
        self.entries = {}
        for label in labels:
            tk.Label(frame, text=label, bg='grey').pack(pady=5)
            entry = tk.Entry(frame)
            entry.pack(pady=5)
            self.entries[label] = entry

        self.message_label = tk.Label(frame, text="", fg="red", bg='grey')
        self.message_label.pack(pady=5)
        self.message_label.pack_forget()

        tk.Button(frame, text="Ajouter Joueur", command=lambda: Joueur.ajouter_joueur(
            self.entries, self.joueurs, self.message_label
        )).pack(pady=5)

        tk.Label(frame, text="Supprimer un joueur (Nom et Prénom)", bg='grey').pack(pady=5)
        self.supprimer_nom_entry = tk.Entry(frame)
        self.supprimer_nom_entry.pack(pady=5)
        self.supprimer_prenom_entry = tk.Entry(frame)
        self.supprimer_prenom_entry.pack(pady=5)
        tk.Button(frame, text="Supprimer Joueur", command=lambda: Joueur.supprimer_joueur(
            self.supprimer_nom_entry, self.supprimer_prenom_entry, self.joueurs, self.message_label
        )).pack(pady=5)

        return frame

    def frame_equipe(self):
        frame = tk.Frame(self.main_window, bg='grey')

        tk.Label(frame, text="Ajouter une equipe", bg='grey').pack(pady=5)
        self.equipe_entry = tk.Entry(frame)
        self.equipe_entry.pack(pady=5)
        tk.Button(frame, text="Ajouter equipe").pack(pady=5)

        tk.Label(frame, text="Supprimer une equipe", bg='grey').pack(pady=5)
        self.supprimer_equipe_entry = tk.Entry(frame)
        self.supprimer_equipe_entry.pack(pady=5)
        tk.Button(frame, text="Supprimer equipe").pack(pady=5)

        return frame

    def show_frame(self, frame_name):
        frame = self.frames[frame_name]
        frame.tkraise()
