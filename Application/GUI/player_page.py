from tkinter import Toplevel, Label, Entry, Button, messagebox
from classes.player import Player

class PlayerPage:
    def __init__(self, gui_manager):
        self.gui_manager = gui_manager

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

            if any(not field for field in [person_ID, last_name, first_name, birth_date, salary, contract, address, phone_number, position, jersey_number]):
                messagebox.showerror("Erreur", "Tous les champs sont obligatoires.")
                return

            if joueur is None and any(j.player_ID == person_ID for j in self.gui_manager.joueurs):
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

        fields = [
            ("ID", "person_ID", int),
            ("Nom", "last_name", str),
            ("Prénom", "first_name", str),
            ("Date de Naissance (YYYY-MM-DD)", "birth_date", str),
            ("Salaire", "salary", float),
            ("Contrat (YYYY-MM-DD)", "contract", str),
            ("Adresse", "address", str),
            ("Téléphone", "phone_number", str),
            ("Poste", "position", str),
            ("Numéro de Maillot", "jersey_number", int)
        ]

        entries = {}
        for i, (label_text, field_name, field_type) in enumerate(fields):
            Label(form_window, text=label_text).grid(row=i, column=0)
            entry = Entry(form_window)
            entry.grid(row=i, column=1)
            if joueur:
                entry.insert(0, getattr(joueur, field_name))
                if field_name == "person_ID":
                    entry.config(state='disabled')
            entries[field_name] = entry

        entry_id = entries["person_ID"]
        entry_last_name = entries["last_name"]
        entry_first_name = entries["first_name"]
        entry_birth_date = entries["birth_date"]
        entry_salary = entries["salary"]
        entry_contract = entries["contract"]
        entry_address = entries["address"]
        entry_phone_number = entries["phone_number"]
        entry_position = entries["position"]
        entry_jersey_number = entries["jersey_number"]

        Button(form_window, text="Modifier" if joueur else "Ajouter", command=submit).grid(row=len(fields), column=0, columnspan=2)

    def add_joueur(self):
        self.open_joueur_form()

    def modify_joueur(self):
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
            else:
                messagebox.showerror("Erreur", "Joueur non trouvé")
        else:
            messagebox.showerror("Erreur", "Aucun joueur sélectionné")
