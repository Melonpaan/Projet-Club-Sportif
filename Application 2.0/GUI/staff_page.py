from tkinter import simpledialog, messagebox
from classes.staff import Staff
from utils import Utils

class StaffPage:
    """
    Classe pour gérer les interactions de la page du staff, y compris l'ajout, la modification et la suppression des membres du staff.
    """
    def __init__(self, gui_manager):
        """
        Initialise StaffPage avec une référence au gestionnaire de l'interface graphique.

        Args:
            gui_manager (GUIManager): Instance du gestionnaire de l'interface graphique.
        """
        self.gui_manager = gui_manager

    def add_staff(self):
        """
        Ajoute un nouveau membre du staff après avoir demandé les détails nécessaires via des boîtes de dialogue.
        """
        person_ID = simpledialog.askinteger("ID", "Entrez l'ID du staff")
        if not person_ID:
            messagebox.showerror("Erreur", "L'ID est obligatoire.")
            return

        if any(staff.person_ID == person_ID for staff in self.gui_manager.staff_members):
            messagebox.showerror("Erreur", "Un staff avec cet ID existe déjà.")
            return

        last_name = simpledialog.askstring("Nom", "Entrez le nom du staff")
        if not last_name:
            messagebox.showerror("Erreur", "Le nom est obligatoire.")
            return

        first_name = simpledialog.askstring("Prénom", "Entrez le prénom du staff")
        if not first_name:
            messagebox.showerror("Erreur", "Le prénom est obligatoire.")
            return

        birth_date = simpledialog.askstring("Date de Naissance", "Entrez la date de naissance (YYYY-MM-DD)")
        if not birth_date:
            messagebox.showerror("Erreur", "La date de naissance est obligatoire.")
            return

        salary = simpledialog.askfloat("Salaire", "Entrez le salaire du staff")
        if salary is None:
            messagebox.showerror("Erreur", "Le salaire est obligatoire.")
            return

        contract = simpledialog.askstring("Contrat", "Entrez la date de fin de contrat (YYYY-MM-DD)")
        if not contract:
            messagebox.showerror("Erreur", "La date de fin de contrat est obligatoire.")
            return

        address = simpledialog.askstring("Adresse", "Entrez l'adresse du staff")
        if not address:
            messagebox.showerror("Erreur", "L'adresse est obligatoire.")
            return

        phone_number = simpledialog.askstring("Téléphone", "Entrez le numéro de téléphone")
        if not phone_number:
            messagebox.showerror("Erreur", "Le numéro de téléphone est obligatoire.")
            return

        role = simpledialog.askstring("Rôle", "Entrez le rôle du staff")
        if not role:
            messagebox.showerror("Erreur", "Le rôle est obligatoire.")
            return

        new_staff = Staff(person_ID, last_name, first_name, birth_date, salary, contract, address, phone_number, role)
        self.gui_manager.staff_members.append(new_staff)
        self.gui_manager.update_staff_treeview()
        Staff.save_to_file(self.gui_manager.staff_members) 

    def modify_staff(self):
        """
        Modifie les informations du membre du staff sélectionné dans le Treeview des staffs.
        Si aucun staff n'est sélectionné ou si le staff n'est pas trouvé, un message d'erreur est affiché.
        """
        selected_item = self.gui_manager.tree_staff.selection()
        if selected_item:
            item = self.gui_manager.tree_staff.item(selected_item)
            values = item['values']
            person_ID = values[0]
            staff = next((s for s in self.gui_manager.staff_members if s.person_ID == person_ID), None)
            if staff:
                staff.last_name = simpledialog.askstring("Nom", "Entrez le nom du staff", initialvalue=staff.last_name)
                staff.first_name = simpledialog.askstring("Prénom", "Entrez le prénom du staff", initialvalue=staff.first_name)
                staff.birth_date = simpledialog.askstring("Date de Naissance", "Entrez la date de naissance (YYYY-MM-DD)", initialvalue=staff.birth_date)
                staff.salary = simpledialog.askfloat("Salaire", "Entrez le salaire du staff", initialvalue=staff.salary)
                staff.contract = simpledialog.askstring("Contrat", "Entrez la date de fin de contrat (YYYY-MM-DD)", initialvalue=staff.contract)
                staff.address = simpledialog.askstring("Adresse", "Entrez l'adresse du staff", initialvalue=staff.address)
                staff.phone_number = simpledialog.askstring("Téléphone", "Entrez le numéro de téléphone", initialvalue=staff.phone_number)
                staff.role = simpledialog.askstring("Rôle", "Entrez le rôle du staff", initialvalue=staff.role)
                
                self.gui_manager.update_staff_treeview()
                Staff.save_to_file(self.gui_manager.staff_members)  
            else:
                messagebox.showerror("Erreur", "Staff non trouvé")
        else:
            messagebox.showerror("Erreur", "Aucun staff sélectionné")

    def delete_staff(self):
        """
        Supprime le membre du staff sélectionné dans le Treeview des staffs après confirmation.
        Si aucun staff n'est sélectionné ou si le staff n'est pas trouvé, un message d'erreur est affiché.
        """
        selected_item = self.gui_manager.tree_staff.selection()
        if selected_item:
            item = self.gui_manager.tree_staff.item(selected_item)
            values = item['values']
            person_ID = values[0]
            self.gui_manager.staff_members = [s for s in self.gui_manager.staff_members if s.person_ID != person_ID]
            self.gui_manager.update_staff_treeview()
            Staff.save_to_file(self.gui_manager.staff_members)  
        else:
            messagebox.showerror("Erreur", "Aucun staff sélectionné")


