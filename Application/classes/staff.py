from tkinter import simpledialog, messagebox
from classes.person import Person
from classes.data_manager import DataManager

class Staff(Person):
    def __init__(self, person_ID, last_name, first_name, birth_date, salary, contract, address, phone_number, role):
        super().__init__(person_ID, last_name, first_name, birth_date, salary, contract, address, phone_number)
        self.role = role

    def to_dict(self):
        data = super().to_dict()
        data.update({
            'role': self.role
        })
        return data

    @classmethod
    def from_dict(cls, data):
        return cls(
            data['person_ID'], data['last_name'], data['first_name'],
            data['birth_date'], data['salary'], data['contract'],
            data['address'], data['phone_number'], data['role']
        )

    @staticmethod
    def save_to_file(staff_members):
        DataManager.save_to_file([staff.to_dict() for staff in staff_members], 'data/staff.json')

    @staticmethod
    def load_from_file():
        staff_data = DataManager.load_from_file('data/staff.json')
        return [Staff.from_dict(data) for data in staff_data]

    @staticmethod
    def add_staff(gui_manager):
        person_ID = simpledialog.askinteger("ID", "Entrez l'ID du staff")
        if not person_ID:
            messagebox.showerror("Erreur", "L'ID est obligatoire.")
            return

        if any(staff.person_ID == person_ID for staff in gui_manager.staff_members):
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
        gui_manager.staff_members.append(new_staff)
        gui_manager.update_staff_treeview()
        Staff.save_to_file(gui_manager.staff_members) 

    @staticmethod
    def modify_staff(gui_manager):
        selected_item = gui_manager.tree_staff.selection()
        if selected_item:
            item = gui_manager.tree_staff.item(selected_item)
            values = item['values']
            person_ID = values[0]
            staff = next((s for s in gui_manager.staff_members if s.person_ID == person_ID), None)
            if staff:
                staff.last_name = simpledialog.askstring("Nom", "Entrez le nom du staff", initialvalue=staff.last_name)
                staff.first_name = simpledialog.askstring("Prénom", "Entrez le prénom du staff", initialvalue=staff.first_name)
                staff.birth_date = simpledialog.askstring("Date de Naissance", "Entrez la date de naissance (YYYY-MM-DD)", initialvalue=staff.birth_date)
                staff.salary = simpledialog.askfloat("Salaire", "Entrez le salaire du staff", initialvalue=staff.salary)
                staff.contract = simpledialog.askstring("Contrat", "Entrez la date de fin de contrat (YYYY-MM-DD)", initialvalue=staff.contract)
                staff.address = simpledialog.askstring("Adresse", "Entrez l'adresse du staff", initialvalue=staff.address)
                staff.phone_number = simpledialog.askstring("Téléphone", "Entrez le numéro de téléphone", initialvalue=staff.phone_number)
                staff.role = simpledialog.askstring("Rôle", "Entrez le rôle du staff", initialvalue=staff.role)
                
                gui_manager.update_staff_treeview()
                Staff.save_to_file(gui_manager.staff_members)  
            else:
                messagebox.showerror("Erreur", "Staff non trouvé")
        else:
            messagebox.showerror("Erreur", "Aucun staff sélectionné")
    
    @staticmethod
    def delete_staff(gui_manager):
        selected_item = gui_manager.tree_staff.selection()
        if selected_item:
            item = gui_manager.tree_staff.item(selected_item)
            values = item['values']
            person_ID = values[0]
            gui_manager.staff_members = [s for s in gui_manager.staff_members if s.person_ID != person_ID]
            gui_manager.update_staff_treeview()
            Staff.save_to_file(gui_manager.staff_members)  
        else:
            messagebox.showerror("Erreur", "Aucun staff sélectionné")