from tkinter import simpledialog, messagebox
from classes.player import Player

class PlayerPage:
    @staticmethod
    def add_joueur(gui_manager):
        person_ID = simpledialog.askinteger("ID", "Entrez l'ID du joueur")
        if not person_ID:
            messagebox.showerror("Erreur", "L'ID est obligatoire.")
            return

        
        if any(joueur.person_ID == person_ID for joueur in gui_manager.joueurs):
            messagebox.showerror("Erreur", "Un joueur avec cet ID existe déjà.")
            return

        last_name = simpledialog.askstring("Nom", "Entrez le nom du joueur")
        if not last_name:
            messagebox.showerror("Erreur", "Le nom est obligatoire.")
            return

        first_name = simpledialog.askstring("Prénom", "Entrez le prénom du joueur")
        if not first_name:
            messagebox.showerror("Erreur", "Le prénom est obligatoire.")
            return

        birth_date = simpledialog.askstring("Date de Naissance", "Entrez la date de naissance (YYYY-MM-DD)")
        if not birth_date:
            messagebox.showerror("Erreur", "La date de naissance est obligatoire.")
            return

        salary = simpledialog.askfloat("Salaire", "Entrez le salaire du joueur")
        if salary is None:
            messagebox.showerror("Erreur", "Le salaire est obligatoire.")
            return

        contract = simpledialog.askstring("Contrat", "Entrez la date de fin de contrat (YYYY-MM-DD)")
        if not contract:
            messagebox.showerror("Erreur", "La date de fin de contrat est obligatoire.")
            return

        address = simpledialog.askstring("Adresse", "Entrez l'adresse du joueur")
        if not address:
            messagebox.showerror("Erreur", "L'adresse est obligatoire.")
            return

        phone_number = simpledialog.askstring("Téléphone", "Entrez le numéro de téléphone")
        if not phone_number:
            messagebox.showerror("Erreur", "Le numéro de téléphone est obligatoire.")
            return

        position = simpledialog.askstring("Poste", "Entrez le poste du joueur")
        if not position:
            messagebox.showerror("Erreur", "Le poste est obligatoire.")
            return

        jersey_number = simpledialog.askinteger("Numéro de Maillot", "Entrez le numéro de maillot du joueur")
        if jersey_number is None:
            messagebox.showerror("Erreur", "Le numéro de maillot est obligatoire.")
            return

        new_joueur = Player(person_ID, last_name, first_name, birth_date, salary, contract, address, phone_number, position, jersey_number)
        gui_manager.joueurs.append(new_joueur)
        gui_manager.update_joueurs_treeview()
        Player.save_to_file(gui_manager.joueurs) 

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
                Player.save_to_file(gui_manager.joueurs) 
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
            Player.save_to_file(gui_manager.joueurs) 
        else:
            messagebox.showerror("Erreur", "Aucun joueur sélectionné")
