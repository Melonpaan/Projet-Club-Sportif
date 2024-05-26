# src/gui/staff_dialogs.py
import tkinter as tk
from tkinter import simpledialog, messagebox
from datetime import date


class AddStaffDialog(simpledialog.Dialog):
    def __init__(self, parent, data_manager, callback):
        self.data_manager = data_manager
        self.callback = callback
        super().__init__(parent, "Ajouter Staff")

    def body(self, master):
        tk.Label(master, text="ID").grid(row=0)
        tk.Label(master, text="Nom").grid(row=1)
        tk.Label(master, text="Prénom").grid(row=2)
        tk.Label(master, text="Date de Naissance (YYYY-MM-DD)").grid(row=3)
        tk.Label(master, text="Rôle").grid(row=4)
        tk.Label(master, text="Salaire").grid(row=5)

        self.entry_id = tk.Entry(master)
        self.entry_last_name = tk.Entry(master)
        self.entry_first_name = tk.Entry(master)
        self.entry_birth_date = tk.Entry(master)
        self.entry_role = tk.Entry(master)
        self.entry_salary = tk.Entry(master)

        self.entry_id.grid(row=0, column=1)
        self.entry_last_name.grid(row=1, column=1)
        self.entry_first_name.grid(row=2, column=1)
        self.entry_birth_date.grid(row=3, column=1)
        self.entry_role.grid(row=4, column=1)
        self.entry_salary.grid(row=5, column=1)

        return self.entry_id  # initial focus

    def validate(self):
        try:
            self.staff_id = int(self.entry_id.get())
            self.last_name = self.entry_last_name.get()
            self.first_name = self.entry_first_name.get()
            self.birth_date = date.fromisoformat(self.entry_birth_date.get())
            self.role = self.entry_role.get()
            self.salary = float(self.entry_salary.get())
            return True
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer des informations valides.")
            return False

    def apply(self):
        staff = {
            "person_id": self.staff_id,
            "last_name": self.last_name,
            "first_name": self.first_name,
            "birth_date": self.birth_date.isoformat(),
            "role": self.role,
            "salary": self.salary,
            "age": self.calculate_age(self.birth_date)
        }
        staff_members = self.data_manager.load_staff()
        staff_members.append(staff)
        self.data_manager.save_staff(staff_members)
        self.callback()

    def calculate_age(self, birth_date):
        today = date.today()
        return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))


class EditStaffDialog(simpledialog.Dialog):
    def __init__(self, parent, data_manager, staff_id, callback):
        self.data_manager = data_manager
        self.staff_id = staff_id
        self.callback = callback
        super().__init__(parent, "Modifier Staff")

    def body(self, master):
        staff = self.get_staff_by_id(self.staff_id)
        if not staff:
            messagebox.showerror("Erreur", "Staff non trouvé.")
            self.destroy()
            return

        tk.Label(master, text="ID").grid(row=0)
        tk.Label(master, text="Nom").grid(row=1)
        tk.Label(master, text="Prénom").grid(row=2)
        tk.Label(master, text="Date de Naissance (YYYY-MM-DD)").grid(row=3)
        tk.Label(master, text="Rôle").grid(row=4)
        tk.Label(master, text="Salaire").grid(row=5)

        self.entry_id = tk.Entry(master)
        self.entry_last_name = tk.Entry(master)
        self.entry_first_name = tk.Entry(master)
        self.entry_birth_date = tk.Entry(master)
        self.entry_role = tk.Entry(master)
        self.entry_salary = tk.Entry(master)

        self.entry_id.insert(0, staff['person_id'])
        self.entry_id.config(state='disabled')  # ID should not be editable
        self.entry_last_name.insert(0, staff['last_name'])
        self.entry_first_name.insert(0, staff['first_name'])
        self.entry_birth_date.insert(0, staff['birth_date'])
        self.entry_role.insert(0, staff['role'])
        self.entry_salary.insert(0, staff['salary'])

        self.entry_id.grid(row=0, column=1)
        self.entry_last_name.grid(row=1, column=1)
        self.entry_first_name.grid(row=2, column=1)
        self.entry_birth_date.grid(row=3, column=1)
        self.entry_role.grid(row=4, column=1)
        self.entry_salary.grid(row=5, column=1)

        return self.entry_last_name  # initial focus

    def validate(self):
        try:
            self.new_last_name = self.entry_last_name.get()
            self.new_first_name = self.entry_first_name.get()
            self.new_birth_date = date.fromisoformat(self.entry_birth_date.get())
            self.new_role = self.entry_role.get()
            self.new_salary = float(self.entry_salary.get())
            return True
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer des informations valides.")
            return False

    def apply(self):
        staff_members = self.data_manager.load_staff()
        for staff in staff_members:
            if staff['person_id'] == self.staff_id:
                staff['last_name'] = self.new_last_name
                staff['first_name'] = self.new_first_name
                staff['birth_date'] = self.new_birth_date.isoformat()
                staff['role'] = self.new_role
                staff['salary'] = self.new_salary
                staff['age'] = self.calculate_age(self.new_birth_date)
                break

        self.data_manager.save_staff(staff_members)
        self.callback()

    def get_staff_by_id(self, staff_id):
        staff_members = self.data_manager.load_staff()
        for staff in staff_members:
            if staff['person_id'] == staff_id:
                return staff
        return None

    def calculate_age(self, birth_date):
        today = date.today()
        return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
