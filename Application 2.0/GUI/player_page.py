from tkinter import Toplevel, Label, Entry, Button, messagebox, ttk
from classes.player import Player
from classes.contract import Contract
from datetime import datetime

class PlayerPage:
    def __init__(self, gui_manager):
        self.gui_manager = gui_manager

    def create_form_widget(self, parent, label_text, row, default_value=None, disabled=False):
        Label(parent, text=label_text).grid(row=row, column=0)
        entry = Entry(parent)
        entry.grid(row=row, column=1)
        if default_value:
            entry.insert(0, default_value)
        if disabled:
            entry.config(state='disabled')
        return entry

    def create_combobox(self, parent, label_text, row, values, default_value=None):
        Label(parent, text=label_text).grid(row=row, column=0)
        combobox = ttk.Combobox(parent, values=values)
        combobox.grid(row=row, column=1)
        if default_value:
            combobox.set(default_value)
        return combobox

    def open_form_widget(self, player=None):
        """
        Méthode pour ajouter ou modifier un joueur suivant si player est donné.
        """
        def player_exists(last_name, first_name, birth_date):
            """Check if a player with the same name and birth date already exists."""
            for p in self.gui_manager.players:
                if p.last_name == last_name and p.first_name == first_name and p.birth_date == birth_date:
                    return True
            return False

        def submit():
            """Méthode permettant de soumettre les données entrées"""
            last_name = entry_last_name.get()
            first_name = entry_first_name.get()
            birth_date = entry_birth_date.get()
            salary = entry_salary.get()
            contract_start = entry_contract_start.get()
            contract_end = entry_contract_end.get()
            address = entry_address.get()
            phone_number = entry_phone_number.get()
            position = entry_position.get()
            jersey_number = entry_jersey_number.get()
            gender = entry_gender.get()

            if not last_name.isalpha():
                messagebox.showerror("Erreur", "Le nom de famille doit être composé uniquement de lettres.")
                return
            if not first_name.isalpha():
                messagebox.showerror("Erreur", "Le prénom doit être composé uniquement de lettres.")
                return

            try:
                datetime.strptime(birth_date, '%d-%m-%Y')
            except ValueError:
                messagebox.showerror("Erreur", "Le format de la date de naissance doit être JJ-MM-AAAA.")
                return

            if not salary.isdigit():
                messagebox.showerror("Erreur", "Le salaire doit être un nombre.")
                return
            if not phone_number.isdigit():
                messagebox.showerror("Erreur", "Le numéro de téléphone doit contenir uniquement des chiffres.")
                return
            if not jersey_number.isdigit():
                messagebox.showerror("Erreur", "Le numéro de maillot doit être un nombre.")
                return

            if player is None and player_exists(last_name, first_name, birth_date):
                messagebox.showerror("Erreur", "Un joueur avec le même nom et date de naissance existe déjà.")
                return

            contract = Contract(contract_start, contract_end, salary)

            # Crée ou met à jour l'objet player
            if player is None:
                new_player = Player.create_new(last_name, first_name, birth_date, contract, address, phone_number, position, jersey_number, gender)
                self.gui_manager.players.append(new_player)
                messagebox.showinfo("Information", f"Joueur ajouté avec l'ID {new_player.person_ID}")
            else:
                player.update_details(last_name, first_name, birth_date, contract, address, phone_number, position, jersey_number, gender)
                messagebox.showinfo("Information", f"Joueur modifié avec l'ID {player.person_ID}")

            # Mettre à jour l'interface avec les infos et enregistrer les modifications
            self.gui_manager.update_players_treeview()
            Player.save_to_file(self.gui_manager.players)
            form_window.destroy()

        # Set up le formulaire, Toplevel permet de créer une page au-dessus d'une autre page
        form_window = Toplevel(self.gui_manager)
        form_window.title("Modifier un joueur" if player else "Ajouter un joueur")

        # Création des entrées pour le formulaire vide ou rempli suivant si l'objet player est donné.
        entry_last_name = self.create_form_widget(form_window, "Nom", 1, getattr(player, 'last_name', ''))
        entry_first_name = self.create_form_widget(form_window, "Prénom", 2, getattr(player, 'first_name', ''))
        entry_birth_date = self.create_form_widget(form_window, "Date de Naissance (JJ-MM-AAAA)", 3, getattr(player, 'birth_date', ''))

        if player:
            salary = player.contract.salary
            contract_start = player.contract.start_date
            contract_end = player.contract.end_date
        else:
            salary = ''
            contract_start = ''
            contract_end = ''

        entry_salary = self.create_form_widget(form_window, "Salaire", 4, salary)
        entry_contract_start = self.create_form_widget(form_window, "Début du Contrat (JJ-MM-AAAA)", 5, contract_start)
        entry_contract_end = self.create_form_widget(form_window, "Fin du Contrat (JJ-MM-AAAA)", 6, contract_end)

        entry_address = self.create_form_widget(form_window, "Adresse", 7, getattr(player, 'address', ''))
        entry_phone_number = self.create_form_widget(form_window, "Téléphone", 8, getattr(player, 'phone_number', ''))

        # Utiliser un Combobox pour le champ "Poste"
        Label(form_window, text="Poste").grid(row=9, column=0)
        entry_position = ttk.Combobox(form_window, values=["Attaquant", "Milieu", "Défenseur", "Gardien"])
        entry_position.grid(row=9, column=1)
        if player:
            entry_position.set(player.position)

        entry_jersey_number = self.create_form_widget(form_window, "Numéro de Maillot", 10, getattr(player, 'jersey_number', ''))

        # Utiliser un Combobox pour le champ "Genre"
        Label(form_window, text="Genre").grid(row=11, column=0)
        entry_gender = ttk.Combobox(form_window, values=["Masculin", "Féminin"])
        entry_gender.grid(row=11, column=1)
        if player:
            entry_gender.set(player.gender)

        # Bouton pour soumettre le formulaire
        Button(form_window, text="Modifier" if player else "Ajouter", command=submit).grid(row=12, column=0, columnspan=2)

    def add_player(self):
        self.open_form_widget()

    def modify_player(self):
        """Modifie les données d'un joueur. On choisit un joueur puis on récupère ses données"""
        selected_item = self.gui_manager.tree_players.selection()
        if selected_item:
            item = self.gui_manager.tree_players.item(selected_item)
            values = item['values']
            person_ID = str(values[0])  # La conversion garantit la comparaison correcte de person_id avec l'objet player
            player = None
            for data in self.gui_manager.players:
                if str(data.person_ID) == person_ID:
                    player = data
                    break
            self.open_form_widget(player)
        else:
            messagebox.showerror("Erreur", "Aucun joueur sélectionné")

    def delete_player(self):
        """Supprime un joueur sélectionné. On choisit un joueur puis on le supprime de la liste."""
        selected_item = self.gui_manager.tree_players.selection()
        if selected_item:
            item = self.gui_manager.tree_players.item(selected_item)
            values = item['values']
            person_ID = str(values[0])  # La conversion garantit la comparaison correcte de person_id avec l'objet player
            player = None
            for data in self.gui_manager.players:
                if str(data.person_ID) == person_ID:
                    player = data
                    break

            if player:
                # Confirmer la suppression
                confirmation = messagebox.askyesno("Confirmation", "Êtes-vous sûr de vouloir supprimer ce joueur ?")
                if confirmation:
                    Player.delete(player)  # Ajoute l'ID du joueur à la liste des IDs disponibles
                    self.gui_manager.players.remove(player)
                    self.gui_manager.update_players_treeview()
                    Player.save_to_file(self.gui_manager.players)
                    messagebox.showinfo("Joueur supprimé", "Le joueur a été supprimé avec succès.")
        else:
            messagebox.showerror("Erreur", "Aucun joueur sélectionné")
