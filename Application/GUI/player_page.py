from tkinter import Toplevel, Label, Entry, Button, messagebox
from classes.player import Player

class PlayerPage:
    def __init__(self, gui_manager):
        self.gui_manager = gui_manager

    def create_form_field(self, parent, label_text, row, default_value=None, disabled=False):
        Label(parent, text=label_text).grid(row=row, column=0)
        entry = Entry(parent)
        entry.grid(row=row, column=1)
        if default_value:
            entry.insert(0, default_value)
            if disabled:
                entry.config(state='disabled')
        return entry

    def open_joueur_form(self, joueur=None):
        def submit():
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

            required_fields = [person_ID, last_name, first_name, birth_date, salary, contract, address, phone_number, position, jersey_number]
            if any(not field for field in required_fields):
                messagebox.showerror("Erreur", "Tous les champs sont obligatoires.")
                return

            if joueur is None:
                if any(j.player_ID == person_ID for j in self.gui_manager.joueurs):
                    messagebox.showerror("Erreur", "Un joueur avec cet ID existe déjà.")
                    return
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

        entry_id = self.create_form_field(form_window, "ID", 0, getattr(joueur, 'person_ID', ''), disabled=bool(joueur))
        entry_last_name = self.create_form_field(form_window, "Nom", 1, getattr(joueur, 'last_name', ''))
        entry_first_name = self.create_form_field(form_window, "Prénom", 2, getattr(joueur, 'first_name', ''))
        entry_birth_date = self.create_form_field(form_window, "Date de Naissance (YYYY-MM-DD)", 3, getattr(joueur, 'birth_date', ''))
        entry_salary = self.create_form_field(form_window, "Salaire", 4, getattr(joueur, 'salary', ''))
        entry_contract = self.create_form_field(form_window, "Contrat (YYYY-MM-DD)", 5, getattr(joueur, 'contract', ''))
        entry_address = self.create_form_field(form_window, "Adresse", 6, getattr(joueur, 'address', ''))
        entry_phone_number = self.create_form_field(form_window, "Téléphone", 7, getattr(joueur, 'phone_number', ''))
        entry_position = self.create_form_field(form_window, "Poste", 8, getattr(joueur, 'position', ''))
        entry_jersey_number = self.create_form_field(form_window, "Numéro de Maillot", 9, getattr(joueur, 'jersey_number', ''))

        Button(form_window, text="Modifier" if joueur else "Ajouter", command=submit).grid(row=10, column=0, columnspan=2)

    def add_joueur(self):
        self.open_joueur_form()

    def modify_joueur(self):
        selected_item = self.gui_manager.tree_joueurs.selection()
        if selected_item:
            item = self.gui_manager.tree_joueurs.item(selected_item)
            values = item['values']
            person_ID = values[0]
            joueur_found = False
            for j in self.gui_manager.joueurs:
                if j.person_ID == person_ID:
                    self.open_joueur_form(j)
                    joueur_found = True
        else:
            messagebox.showerror("Erreur", "Aucun joueur sélectionné")

    def delete_joueur(self):
        selected_item = self.gui_manager.tree_joueurs.selection()
        if selected_item:
            item = self.gui_manager.tree_joueurs.item(selected_item)
            values = item['values']
            person_ID = values[0]
            joueur_found = False
            new_joueurs_list = []

            for j in self.gui_manager.joueurs:
                if j.person_ID == person_ID:
                    joueur_found = True
                else:
                    new_joueurs_list.append(j)

            if joueur_found:
                self.gui_manager.joueurs = new_joueurs_list
                self.gui_manager.update_joueurs_treeview()
                Player.save_to_file(self.gui_manager.joueurs)
                messagebox.showinfo("Joueur supprimé", "Le joueur a été supprimé avec succès.")
            else:
                messagebox.showerror("Erreur", "Joueur non trouvé")
        else:
            messagebox.showerror("Erreur", "Aucun joueur sélectionné")