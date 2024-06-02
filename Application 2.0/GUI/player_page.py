from tkinter import Toplevel, messagebox
from classes.player import Player
from utils import Utils

class PlayerPage:
    """
    Classe pour gérer les interactions de la page des joueurs, y compris l'ajout, la modification et la suppression de joueurs.
    """
    def __init__(self, gui_manager):
        """
        Initialise PlayerPage avec une référence au gestionnaire de l'interface graphique.

        Args:
            gui_manager (GUIManager): Instance du gestionnaire de l'interface graphique.
        """
        self.gui_manager = gui_manager

    def open_joueur_form(self, joueur=None):
        """
        Ouvre une fenêtre de formulaire pour ajouter ou modifier un joueur.

        Args:
            joueur (Player, optional): Instance du joueur à modifier. Si None, un nouveau joueur sera ajouté.
        """
        def submit():
            """
            Soumet le formulaire de joueur et met à jour les informations du joueur ou ajoute un nouveau joueur.
            """
            try:
                person_ID = int(entry_id.get())
                last_name = entry_last_name.get()
                first_name = entry_first_name.get()
                birth_date = entry_birth_date.get()
                salary = float(entry_salary.get())
                contract = entry_contract.get()
                address = entry_address.get()
                phone_number = entry_phone_number.get()
                position = entry_position.get()
                jersey_number = int(entry_jersey_number.get())
            except ValueError:
                messagebox.showerror("Erreur", "Veuillez entrer des valeurs valides.")
                return

            if any(not field for field in [person_ID, last_name, first_name, birth_date, salary, contract, address, phone_number, position, jersey_number]):
                messagebox.showerror("Erreur", "Tous les champs sont obligatoires.")
                return

            if joueur is None and any(j.person_ID == person_ID for j in self.gui_manager.joueurs):
                messagebox.showerror("Erreur", "Un joueur avec cet ID existe déjà.")
                return

            if joueur is None:
                new_joueur = Player(person_ID, last_name, first_name, birth_date, salary, contract, address, phone_number, position, jersey_number)
                self.gui_manager.joueurs.append(new_joueur)
            else:
                joueur.person_ID = person_ID
                joueur.last_name = last_name
                joueur.first_name = first_name
                joueur.birth_date = birth_date
                joueur.salary = salary
                joueur.contract = contract
                joueur.address = address
                joueur.phone_number = phone_number
                joueur.position = position
                joueur.jersey_number = jersey_number

            self.gui_manager.update_joueurs_treeview()
            Player.save_to_file(self.gui_manager.joueurs)
            form_window.destroy()

        form_window = Toplevel(self.gui_manager)
        form_window.title("Modifier un joueur" if joueur else "Ajouter un joueur")

        entry_id = Utils.create_label_and_entry(form_window, "ID", 0, getattr(joueur, 'person_ID', ''), disabled=bool(joueur))
        entry_last_name = Utils.create_label_and_entry(form_window, "Nom", 1, getattr(joueur, 'last_name', ''))
        entry_first_name = Utils.create_label_and_entry(form_window, "Prénom", 2, getattr(joueur, 'first_name', ''))
        entry_birth_date = Utils.create_label_and_entry(form_window, "Date de Naissance (YYYY-MM-DD)", 3, getattr(joueur, 'birth_date', ''))
        entry_salary = Utils.create_label_and_entry(form_window, "Salaire", 4, getattr(joueur, 'salary', ''))
        entry_contract = Utils.create_label_and_entry(form_window, "Contrat (YYYY-MM-DD)", 5, getattr(joueur, 'contract', ''))
        entry_address = Utils.create_label_and_entry(form_window, "Adresse", 6, getattr(joueur, 'address', ''))
        entry_phone_number = Utils.create_label_and_entry(form_window, "Téléphone", 7, getattr(joueur, 'phone_number', ''))
        entry_position = Utils.create_label_and_entry(form_window, "Poste", 8, getattr(joueur, 'position', ''))
        entry_jersey_number = Utils.create_label_and_entry(form_window, "Numéro de Maillot", 9, getattr(joueur, 'jersey_number', ''))

        Utils.create_button(form_window, "Modifier" if joueur else "Ajouter", submit, 10, 0, 2)

    def add_joueur(self):
        """
        Ouvre la fenêtre de formulaire pour ajouter un nouveau joueur.
        """
        self.open_joueur_form()

    def modify_joueur(self):
        """
        Ouvre la fenêtre de formulaire pour modifier le joueur sélectionné dans le Treeview des joueurs.
        """
        selected_item = self.gui_manager.tree_joueurs.selection()
        if selected_item:
            item = self.gui_manager.tree_joueurs.item(selected_item)
            values = item['values']
            person_ID = values[0]
            joueur = next((j for j in self.gui_manager.joueurs if j.person_ID == person_ID), None)
            if joueur:
                self.open_joueur_form(joueur)
            else:
                messagebox.showerror("Erreur", "Joueur non trouvé")
        else:
            messagebox.showerror("Erreur", "Aucun joueur sélectionné")

    def delete_joueur(self):
        """
        Supprime le joueur sélectionné dans le Treeview des joueurs après confirmation.
        """
        selected_item = self.gui_manager.tree_joueurs.selection()
        if selected_item:
            item = self.gui_manager.tree_joueurs.item(selected_item)
            values = item['values']
            person_ID = values[0]
            joueur = next((j for j in self.gui_manager.joueurs if j.person_ID == person_ID), None)
            if joueur:
                self.gui_manager.joueurs.remove(joueur)
                self.gui_manager.update_joueurs_treeview()
                Player.save_to_file(self.gui_manager.joueurs)
                messagebox.showinfo("Information", "Joueur supprimé avec succès.")
            else:
                messagebox.showerror("Erreur", "Joueur non trouvé")
        else:
            messagebox.showerror("Erreur", "Aucun joueur sélectionné")


