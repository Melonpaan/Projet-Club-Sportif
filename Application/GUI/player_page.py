from tkinter import simpledialog, messagebox
from classes.player import Player

class PlayerPage:
    @staticmethod
    def add_joueur(gui_manager):
        person_ID = simpledialog.askinteger("ID", "Entrez l'ID du joueur")
        last_name = simpledialog.askstring("Nom", "Entrez le nom du joueur")
        first_name = simpledialog.askstring("Prénom", "Entrez le prénom du joueur")
        birth_date = simpledialog.askstring("Date de Naissance", "Entrez la date de naissance (YYYY-MM-DD)")
        salary = simpledialog.askfloat("Salaire", "Entrez le salaire du joueur")
        contract = simpledialog.askstring("Contrat", "Entrez la date de fin de contrat (YYYY-MM-DD)")
        address = simpledialog.askstring("Adresse", "Entrez l'adresse du joueur")
        phone_number = simpledialog.askstring("Téléphone", "Entrez le numéro de téléphone")
        position = simpledialog.askstring("Poste", "Entrez le poste du joueur")
        jersey_number = simpledialog.askinteger("Numéro de Maillot", "Entrez le numéro de maillot du joueur")
        
        new_joueur = Player(person_ID, last_name, first_name, birth_date, salary, contract, address, phone_number, position, jersey_number)
        gui_manager.joueurs.append(new_joueur)
        gui_manager.update_joueurs_treeview()
        Player.save_to_file(gui_manager.joueurs)  # Enregistrer les joueurs dans le fichier JSON

    @staticmethod
    def modify_joueur(gui_manager):
        selected_item = gui_manager.tree_joueurs.selection()
        if selected_item:
            item = gui_manager.tree_joueurs.item(selected_item)
            values = item['values']
            person_ID = values[0]
            joueur = next((j for j in gui_manager.joueurs if j.person_ID == person_ID), None)
            if joueur:
                joueur.last_name = simpledialog.askstring("Nom", "Entrez le nom du joueur", initialvalue=joueur.last_name)
                joueur.first_name = simpledialog.askstring("Prénom", "Entrez le prénom du joueur", initialvalue=joueur.first_name)
                joueur.birth_date = simpledialog.askstring("Date de Naissance", "Entrez la date de naissance (YYYY-MM-DD)", initialvalue=joueur.birth_date)
                joueur.salary = simpledialog.askfloat("Salaire", "Entrez le salaire du joueur", initialvalue=joueur.salary)
                joueur.contract = simpledialog.askstring("Contrat", "Entrez la date de fin de contrat (YYYY-MM-DD)", initialvalue=joueur.contract)
                joueur.address = simpledialog.askstring("Adresse", "Entrez l'adresse du joueur", initialvalue=joueur.address)
                joueur.phone_number = simpledialog.askstring("Téléphone", "Entrez le numéro de téléphone", initialvalue=joueur.phone_number)
                joueur.position = simpledialog.askstring("Poste", "Entrez le poste du joueur", initialvalue=joueur.position)
                joueur.jersey_number = simpledialog.askinteger("Numéro de Maillot", "Entrez le numéro de maillot du joueur", initialvalue=joueur.jersey_number)
                
                gui_manager.update_joueurs_treeview()
                Player.save_to_file(gui_manager.joueurs)  # Enregistrer les joueurs dans le fichier JSON
            else:
                messagebox.showerror("Erreur", "Joueur non trouvé")
        else:
            messagebox.showerror("Erreur", "Aucun joueur sélectionné")
    
    @staticmethod
    def delete_joueur(gui_manager):
        selected_item = gui_manager.tree_joueurs.selection()
        if selected_item:
            item = gui_manager.tree_joueurs.item(selected_item)
            values = item['values']
            person_ID = values[0]
            gui_manager.joueurs = [j for j in gui_manager.joueurs if j.person_ID != person_ID]
            gui_manager.update_joueurs_treeview()
            Player.save_to_file(gui_manager.joueurs)  # Enregistrer les joueurs dans le fichier JSON
        else:
            messagebox.showerror("Erreur", "Aucun joueur sélectionné")
