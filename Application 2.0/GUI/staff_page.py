from tkinter import Toplevel, Label, Entry, Button, messagebox, ttk
from classes.staff import Staff
from classes.contract import Contract
from datetime import datetime

class StaffPage:
    def __init__(self, gui_manager):
        """
        Initialise la gestion de la page Staff.

        Args:
            gui_manager (GUIManager): Instance de la classe GUIManager pour accéder aux données et méthodes de l'application.
        """
        self.gui_manager = gui_manager

    def create_form_widget(self, parent, label_text, row, default_value=None, disabled=False):
        """
        Crée et configure un champ de formulaire (label + entry) dans une interface Tkinter.

        Args:
            parent (tk.Widget): Le widget parent dans lequel créer le champ de formulaire.
            label_text (str): Le texte de l'étiquette du champ.
            row (int): La ligne dans la grille où placer le champ.
            default_value (str, optional): La valeur par défaut du champ d'entrée.
            disabled (bool, optional): Si True, désactive le champ d'entrée.

        Returns:
            Entry: Le widget d'entrée créé.
        """
        Label(parent, text=label_text).grid(row=row, column=0)
        entry = Entry(parent)
        entry.grid(row=row, column=1)
        if default_value:
            entry.insert(0, default_value)
        if disabled:
            entry.config(state='disabled')
        return entry

    def open_form_widget(self, staff=None):
        """
        Ouvre une fenêtre de formulaire pour ajouter ou modifier un membre du staff.

        Args:
            staff (Staff, optional): Le membre du staff à modifier. Si None, crée un nouveau membre du staff.
        """
        def staff_exists(last_name, first_name, birth_date):
            """
            Vérifie si un membre du staff avec le même nom et la même date de naissance existe déjà.

            Args:
                last_name (str): Le nom de famille du membre du staff.
                first_name (str): Le prénom du membre du staff.
                birth_date (str): La date de naissance du membre du staff.

            Returns:
                bool: True si un membre du staff avec les mêmes informations existe déjà, False sinon.
            """
            for s in self.gui_manager.staff_members:
                if s.last_name == last_name and s.first_name == first_name and s.birth_date == birth_date:
                    return True
            return False

        def submit():
            """
            Soumet les données entrées dans le formulaire et crée ou met à jour un membre du staff.
            """
            last_name = entry_last_name.get()
            first_name = entry_first_name.get()
            birth_date = entry_birth_date.get()
            salary = entry_salary.get()
            contract_start = entry_contract_start.get()
            contract_end = entry_contract_end.get()
            address = entry_address.get()
            phone_number = entry_phone_number.get()
            role = entry_role.get()
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

            if staff is None and staff_exists(last_name, first_name, birth_date):
                messagebox.showerror("Erreur", "Un membre du staff avec le même nom et date de naissance existe déjà.")
                return

            contract = Contract(contract_start, contract_end, salary)

            # Crée ou met à jour l'objet staff
            if staff is None:
                new_staff = Staff.create_new(last_name, first_name, birth_date, contract, address, phone_number, role, gender)
                self.gui_manager.staff_members.append(new_staff)
                messagebox.showinfo("Information", f"Membre du staff ajouté avec l'ID {new_staff.person_ID}")
            else:
                staff.update_details(last_name, first_name, birth_date, contract, address, phone_number, role, gender)
                messagebox.showinfo("Information", f"Membre du staff modifié avec l'ID {staff.person_ID}")

            # Mettre à jour l'interface avec les infos et enregistrer les modifications
            self.gui_manager.update_staff_treeview()
            Staff.save_to_file(self.gui_manager.staff_members)
            form_window.destroy()

        # Set up le formulaire, Toplevel permet de créer une page au-dessus d'une autre page
        form_window = Toplevel(self.gui_manager)
        form_window.title("Modifier un membre du staff" if staff else "Ajouter un membre du staff")

        # Création des entrées pour le formulaire vide ou rempli suivant si l'objet staff est donné
        entry_last_name = self.create_form_widget(form_window, "Nom", 1, getattr(staff, 'last_name', ''))
        entry_first_name = self.create_form_widget(form_window, "Prénom", 2, getattr(staff, 'first_name', ''))
        entry_birth_date = self.create_form_widget(form_window, "Date de Naissance (JJ-MM-AAAA)", 3, getattr(staff, 'birth_date', ''))
        
        if staff:
            salary = staff.contract.salary
            contract_start = staff.contract.start_date
            contract_end = staff.contract.end_date
        else:
            salary = ''
            contract_start = ''
            contract_end = ''

        entry_salary = self.create_form_widget(form_window, "Salaire", 4, salary)
        entry_contract_start = self.create_form_widget(form_window, "Début du Contrat (JJ-MM-AAAA)", 5, contract_start)
        entry_contract_end = self.create_form_widget(form_window, "Fin du Contrat (JJ-MM-AAAA)", 6, contract_end)

        entry_address = self.create_form_widget(form_window, "Adresse", 7, getattr(staff, 'address', ''))
        entry_phone_number = self.create_form_widget(form_window, "Téléphone", 8, getattr(staff, 'phone_number', ''))

        # Utiliser un Combobox pour le champ "Rôle"
        Label(form_window, text="Rôle").grid(row=9, column=0)
        entry_role = ttk.Combobox(form_window, values=["Médecin", "Entraîneur"])
        entry_role.grid(row=9, column=1)
        if staff:
            entry_role.set(staff.role)
        
        # Utiliser un Combobox pour le champ "Genre"
        Label(form_window, text="Genre").grid(row=10, column=0)
        entry_gender = ttk.Combobox(form_window, values=["Masculin", "Féminin"])
        entry_gender.grid(row=10, column=1)
        if staff:
            entry_gender.set(staff.gender)

        # Bouton pour soumettre le formulaire
        Button(form_window, text="Modifier" if staff else "Ajouter", command=submit).grid(row=11, column=0, columnspan=2)

    def add_staff(self):
        """
        Ouvre une fenêtre de formulaire pour ajouter un nouveau membre du staff.
        """
        self.open_form_widget()

    def modify_staff(self):
        """
        Modifie les données d'un membre du staff sélectionné.

        On choisit un membre du staff dans la Treeview, puis on récupère et affiche ses données dans le formulaire.
        """
        selected_item = self.gui_manager.tree_staff.selection()
        if selected_item:
            item = self.gui_manager.tree_staff.item(selected_item)
            values = item['values']
            person_ID = str(values[0])
            staff = None
            for data in self.gui_manager.staff_members:
                if str(data.person_ID) == person_ID:
                    staff = data
                    break
            self.open_form_widget(staff)
        else:
            messagebox.showerror("Erreur", "Aucun membre du staff sélectionné")

    def delete_staff(self):
        """
        Supprime un membre du staff sélectionné.

        On choisit un membre du staff dans la Treeview, puis on le supprime de la liste et des données sauvegardées.
        """
        selected_item = self.gui_manager.tree_staff.selection()
        if selected_item:
            item = self.gui_manager.tree_staff.item(selected_item)
            values = item['values']
            person_ID = str(values[0])
            staff = None
            for data in self.gui_manager.staff_members:
                if str(data.person_ID) == person_ID:
                    staff = data
                    break

            if staff:
                # Confirmer la suppression
                confirmation = messagebox.askyesno("Confirmation", "Êtes-vous sûr de vouloir supprimer ce membre du staff ?")
                if confirmation:
                    Staff.delete(staff)
                    self.gui_manager.staff_members.remove(staff)
                    self.gui_manager.update_staff_treeview()
                    Staff.save_to_file(self.gui_manager.staff_members)
                    messagebox.showinfo("Membre du staff supprimé", "Le membre du staff a été supprimé avec succès.")
            else:
                messagebox.showerror("Erreur", "Aucun membre du staff sélectionné")
