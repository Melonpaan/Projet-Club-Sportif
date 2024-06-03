from tkinter import Toplevel, Label, Entry, Button, messagebox
from classes.staff import Staff
from datetime import datetime

class StaffPage:
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

    def open_form_widget(self, staff=None):
        """Méthode qui permet d'ajouter ou de modifier un membre du staff suivant si staff est donné"""
        def submit():
            """Méthode permettant de soumettre les données entrées"""
            last_name = entry_last_name.get()
            first_name = entry_first_name.get()
            birth_date = entry_birth_date.get()
            salary = entry_salary.get()
            contract = entry_contract.get()
            address = entry_address.get()
            phone_number = entry_phone_number.get()
            role = entry_role.get()

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

            # Crée ou met à jour l'objet staff
            if staff is None:
                new_staff = Staff.create_new(last_name, first_name, birth_date, salary, contract, address, phone_number, role)
                self.gui_manager.staff_members.append(new_staff)
            else:
                staff.update_details(staff.person_ID, last_name, first_name, birth_date, salary, contract, address, phone_number, role)

            # Mettre à jour l'interface avec les infos et enregistrer les modifications
            self.gui_manager.update_staff_treeview()
            Staff.save_to_file(self.gui_manager.staff_members)
            form_window.destroy()

        # Set up le formulaire, Toplevel permet de créer une page au-dessus d'une autre page
        form_window = Toplevel(self.gui_manager)
        form_window.title("Modifier un membre du staff" if staff else "Ajouter un membre du staff")

        # Création des entrées pour le formulaire vide ou rempli suivant si l'objet staff est donné. getattr permet d'accéder à un attribut d'un objet (objet, 'nom_attribut', valeur_attribut)
        entry_id = self.create_form_widget(form_window, "ID", 0, getattr(staff, 'person_ID', ''), disabled=True)
        entry_last_name = self.create_form_widget(form_window, "Nom", 1, getattr(staff, 'last_name', ''))
        entry_first_name = self.create_form_widget(form_window, "Prénom", 2, getattr(staff, 'first_name', ''))
        entry_birth_date = self.create_form_widget(form_window, "Date de Naissance (JJ-MM-AAAA)", 3, getattr(staff, 'birth_date', ''))
        entry_salary = self.create_form_widget(form_window, "Salaire", 4, getattr(staff, 'salary', ''))
        entry_contract = self.create_form_widget(form_window, "Contrat (JJ-MM-AAAA)", 5, getattr(staff, 'contract', ''))
        entry_address = self.create_form_widget(form_window, "Adresse", 6, getattr(staff, 'address', ''))
        entry_phone_number = self.create_form_widget(form_window, "Téléphone", 7, getattr(staff, 'phone_number', ''))
        entry_role = self.create_form_widget(form_window, "Rôle", 8, getattr(staff, 'role', ''))

        # Bouton pour soumettre le formulaire
        Button(form_window, text="Modifier" if staff else "Ajouter", command=submit).grid(row=9, column=0, columnspan=2)

    def add_staff(self):
        self.open_form_widget()

    def modify_staff(self):
        """Modifie les données d'un membre du staff. On choisit un membre puis on récupère ses données"""
        selected_item = self.gui_manager.tree_staff.selection()
        if selected_item:
            item = self.gui_manager.tree_staff.item(selected_item)
            values = item['values']
            person_ID = str(values[0])  # La conversion garantit la comparaison correcte de person_id avec l'objet staff
            staff = None
            for data in self.gui_manager.staff_members:
                if str(data.person_ID) == person_ID:
                    staff = data
                    break
            self.open_form_widget(staff)
        else:
            messagebox.showerror("Erreur", "Aucun membre du staff sélectionné")

    def delete_staff(self):
        """Supprime un membre du staff sélectionné. On choisit un membre puis on le supprime de la liste."""
        selected_item = self.gui_manager.tree_staff.selection()
        if selected_item:
            item = self.gui_manager.tree_staff.item(selected_item)
            values = item['values']
            person_ID = str(values[0])  # La conversion garantit la comparaison correcte de person_id avec l'objet staff
            staff = None
            for data in self.gui_manager.staff_members:
                if str(data.person_ID) == person_ID:
                    staff = data
                    break

            if staff:
                # Confirmer la suppression
                confirmation = messagebox.askyesno("Confirmation", "Êtes-vous sûr de vouloir supprimer ce membre du staff ?")
                if confirmation:
                    Staff.delete(staff)  # Ajoute l'ID du membre du staff à la liste des IDs disponibles
                    self.gui_manager.staff_members.remove(staff)
                    self.gui_manager.update_staff_treeview()
                    Staff.save_to_file(self.gui_manager.staff_members)
                    messagebox.showinfo("Membre du staff supprimé", "Le membre du staff a été supprimé avec succès.")
        else:
            messagebox.showerror("Erreur", "Aucun membre du staff sélectionné")

