from tkinter import Toplevel, Label, Entry, Button, messagebox
from classes.player import Player
from datetime import datetime

class PlayerPage:
    def __init__(self, gui_manager):
        self.gui_manager = gui_manager

    def create_form_widget(self, parent, label_text, row, default_value=None, disabled=False):
        """Create and configure a form field (label + entry) in a Tkinter GUI."""
        Label(parent, text=label_text).grid(row=row, column=0)
        entry = Entry(parent)
        entry.grid(row=row, column=1)
        if default_value:
            entry.insert(0, default_value)
        if disabled:
            entry.config(state='disabled')
        return entry

    def open_form_widget(self, player=None):
        """Méthode qui permet d'ajouter ou de modifier un joueur suivant si player est donné"""
        def submit():
            """Méthode permettant de soumettre les données entrées"""
            last_name = entry_last_name.get()
            first_name = entry_first_name.get()
            birth_date = entry_birth_date.get()
            salary = entry_salary.get()
            contract = entry_contract.get()
            address = entry_address.get()
            phone_number = entry_phone_number.get()
            position = entry_position.get()
            jersey_number = entry_jersey_number.get()

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

            # Crée ou met à jour l'objet player
            if player is None:
                new_player = Player.create_new(last_name, first_name, birth_date, salary, contract, address, phone_number, position, jersey_number)
                self.gui_manager.players.append(new_player)
            else:
                player.update_details(player.person_ID, last_name, first_name, birth_date, salary, contract, address, phone_number, position, jersey_number)

            # Mettre à jour l'interface avec les infos et enregistrer les modifications
            self.gui_manager.update_players_treeview()
            Player.save_to_file(self.gui_manager.players)
            form_window.destroy()

        # Set up le formulaire, Toplevel permet de créer une page au-dessus d'une autre page
        form_window = Toplevel(self.gui_manager)
        form_window.title("Modifier un joueur" if player else "Ajouter un joueur")

        # Création des entrées pour le formulaire vide ou rempli suivant si l'objet player est donné. getattr permet d'accéder à un attribut d'un objet (objet, 'nom_attribut', valeur_attribut)
        entry_id = self.create_form_widget(form_window, "ID", 0, getattr(player, 'person_ID', ''), disabled=True)
        entry_last_name = self.create_form_widget(form_window, "Nom", 1, getattr(player, 'last_name', ''))
        entry_first_name = self.create_form_widget(form_window, "Prénom", 2, getattr(player, 'first_name', ''))
        entry_birth_date = self.create_form_widget(form_window, "Date de Naissance (JJ-MM-AAAA)", 3, getattr(player, 'birth_date', ''))
        entry_salary = self.create_form_widget(form_window, "Salaire", 4, getattr(player, 'salary', ''))
        entry_contract = self.create_form_widget(form_window, "Contrat (JJ-MM-AAAA)", 5, getattr(player, 'contract', ''))
        entry_address = self.create_form_widget(form_window, "Adresse", 6, getattr(player, 'address', ''))
        entry_phone_number = self.create_form_widget(form_window, "Téléphone", 7, getattr(player, 'phone_number', ''))
        entry_position = self.create_form_widget(form_window, "Poste", 8, getattr(player, 'position', ''))
        entry_jersey_number = self.create_form_widget(form_window, "Numéro de Maillot", 9, getattr(player, 'jersey_number', ''))

        # Bouton pour soumettre le formulaire
        Button(form_window, text="Modifier" if player else "Ajouter", command=submit).grid(row=10, column=0, columnspan=2)


    def add_player(self):
        self.open_form_widget()

    def modify_player(self):
        """modifie les données du joueur. on choisit un joueur puis on recupere ses données"""
        selected_item = self.gui_manager.tree_players.selection()
        if selected_item:
            item = self.gui_manager.tree_players.item(selected_item)
            values = item['values']
            person_ID = str(values[0])  # la conversion garantit la comparaison correcte de person_id avec l'objet player
            player=None
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
