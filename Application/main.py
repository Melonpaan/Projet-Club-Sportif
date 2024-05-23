import tkinter as tk
from joueur import Joueur
import json

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Club de foot')
        self.geometry('1280x720')
        self.frames = {}
        self.joueurs = self.charger_joueurs()

        self.sidebar = tk.Frame(self, width=320, bg='#2e2e2e', height=720,borderwidth=2)
        self.sidebar.pack(expand=False, fill='both', side='left')

        self.main_window= tk.Frame(self, bg='#cccccc', width=960, height=720)
        self.main_window.pack(expand=True, fill='both', side='right')

        self.main_window.grid_rowconfigure(0, weight=1)
        self.main_window.grid_columnconfigure(0, weight=1)

        self.add_sidebar_buttons()

        
        self.create_frame()
  # ---------------------------- Interface ------------------------------- #  
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
        Equipe_frame = self.frame_equipe()

        frames_list = [club_frame,player_frame,Equipe_frame]
        names = ['Club','Player','Equipe']

        for i in range(len(frames_list)):
            F = frames_list[i]
            name = names[i]
            self.frames[name]= F
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

        tk.Button(frame, text="Ajouter Joueur", command=self.ajouter_joueur).pack(pady=5)

        tk.Label(frame, text="Supprimer un joueur (Nom et Prénom)", bg='grey').pack(pady=5)
        self.supprimer_nom_entry = tk.Entry(frame)
        self.supprimer_nom_entry.pack(pady=5)
        self.supprimer_prenom_entry = tk.Entry(frame)
        self.supprimer_prenom_entry.pack(pady=5)
        tk.Button(frame, text="Supprimer Joueur", command=self.supprimer_joueur).pack(pady=5)

        self.message_label = tk.Label(frame, text="", fg="red", bg='grey')
        self.message_label.pack(pady=5)

        return frame
    
    def frame_equipe(self):
        frame =  tk.Frame(self.main_window, bg='grey')

        tk.Label(frame, text="Ajouter une equipe", bg='grey').pack(pady=5)
        self.equipe_entry = tk.Entry(frame)
        self.equipe_entry.pack(pady=5)
        tk.Button(frame, text="Ajouter equipe",).pack(pady=5)

        tk.Label(frame, text="Supprimer une equipe", bg='grey').pack(pady=5)
        self.supprimer_equipe_entry = tk.Entry(frame)
        self.supprimer_equipe_entry.pack(pady=5)
        tk.Button(frame, text="Supprimer equipe").pack(pady=5)

        return frame

    def show_frame(self, frame_name):
        frame = self.frames[frame_name]
        frame.tkraise()
# ---------------------------- Methode ------------------------------- #
    def ajouter_joueur(self):
        details = {}
        for label, entry in self.entries.items():
            details[label] = entry.get()
        
        if not all(details.values()):
            self.message_label.config(text="Erreur: Tous les champs doivent être remplis", fg="red")
           

        if (details["Nom"], details["Prénom"]) in [(joueur.nom, joueur.prenom) for joueur in self.joueurs]:
            self.message_label.config(text="Erreur: Le joueur est déjà dans le club", fg="red")
        else:
            nouveau_joueur = Joueur(
                details["Nom"], details["Prénom"], details["Date de naissance (JJ/MM/AAAA)"],
                details["Poste"], details["Position"], details["Salaire (€)"], details["Contrat (Durée)"]
            )
            self.joueurs.add(nouveau_joueur)
            self.sauvegarder_joueurs()
            self.message_label.config(text="Joueur ajouté avec succès", fg="green")
 
        for entry in self.entries.values():
            entry.delete(0, tk.END)
    def supprimer_joueur(self):
        nom_joueur = self.supprimer_nom_entry.get()
        prenom_joueur = self.supprimer_prenom_entry.get()
        
        joueur_a_supprimer = None
        for joueur in self.joueurs:
            if joueur.nom == nom_joueur and joueur.prenom == prenom_joueur:
                joueur_a_supprimer = joueur
                break  # Une fois que nous trouvons le joueur, nous sortons de la boucle
        
        if joueur_a_supprimer:
            self.joueurs.remove(joueur_a_supprimer)
            self.sauvegarder_joueurs()
            self.message_label.config(text="Joueur supprimé avec succès", fg="green")
        else:
            self.message_label.config(text="Erreur: Le joueur n'est pas dans le club", fg="red")

        self.supprimer_nom_entry.delete(0, tk.END)
        self.supprimer_prenom_entry.delete(0, tk.END)

    
    def sauvegarder_joueurs(self):
        # Convertir les objets joueur en dictionnaires pour la sauvegarde
        joueurs_dict = [joueur.to_dict() for joueur in self.joueurs]

        # Chemin du fichier où les joueurs seront sauvegardés
        fichier_path = "Application/data/joueurs.json"

        # Ouvrir le fichier en mode écriture et sauvegarder les joueurs en format JSON
        with open(fichier_path, "w") as fichier:
            json.dump(joueurs_dict, fichier)

    def charger_joueurs(self):
        try:
            with open("Application/data/joueurs.json", "r") as f:
                joueurs_dict = json.load(f)
            return {Joueur.from_dict(joueur) for joueur in joueurs_dict}
        except (FileNotFoundError, json.JSONDecodeError):
            return set()

            
    


if __name__ == "__main__":
    app = App()
    app.mainloop()