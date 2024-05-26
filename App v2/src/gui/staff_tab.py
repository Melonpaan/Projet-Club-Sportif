# src/gui/staff_tab.py
import tkinter as tk
from tkinter import ttk, messagebox
from src.gui.staff_dialogs import AddStaffDialog, EditStaffDialog


class StaffTab:
    def __init__(self, parent, data_manager):
        self.frame = ttk.Frame(parent)
        self.data_manager = data_manager

        self.create_widgets()
        self.populate_staff_list()

    def create_widgets(self):
        self.tree = ttk.Treeview(self.frame, columns=("ID", "Nom", "Prénom", "Âge", "Rôle", "Salaire"), show='headings')
        for col in ("ID", "Nom", "Prénom", "Âge", "Rôle", "Salaire"):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        self.tree.pack(fill='both', expand=True)

        btn_frame = ttk.Frame(self.frame)
        btn_frame.pack(fill='x')

        self.add_btn = ttk.Button(btn_frame, text="Ajouter Staff", command=self.add_staff)
        self.add_btn.pack(side='left')

        self.edit_btn = ttk.Button(btn_frame, text="Modifier Staff", command=self.edit_staff)
        self.edit_btn.pack(side='left')

        self.delete_btn = ttk.Button(btn_frame, text="Supprimer Staff", command=self.delete_staff)
        self.delete_btn.pack(side='left')

    def populate_staff_list(self):
        self.tree.delete(*self.tree.get_children())  # Clear existing entries
        staff_members = self.data_manager.load_staff()
        for staff in staff_members:
            self.tree.insert("", "end", values=(
            staff['person_id'], staff['last_name'], staff['first_name'], staff['age'], staff['role'], staff['salary']))

    def add_staff(self):
        AddStaffDialog(self.frame, self.data_manager, self.populate_staff_list)

    def edit_staff(self):
        selected_item = self.tree.selection()
        if selected_item:
            staff_id = self.tree.item(selected_item)["values"][0]
            EditStaffDialog(self.frame, self.data_manager, staff_id, self.populate_staff_list)
        else:
            messagebox.showwarning("Attention", "Veuillez sélectionner un membre du staff à modifier.")

    def delete_staff(self):
        selected_item = self.tree.selection()
        if selected_item:
            staff_id = self.tree.item(selected_item)["values"][0]
            staff_members = self.data_manager.load_staff()
            staff_members = [staff for staff in staff_members if staff['person_id'] != staff_id]
            self.data_manager.save_staff(staff_members)
            self.populate_staff_list()
        else:
            messagebox.showwarning("Attention", "Veuillez sélectionner un membre du staff à supprimer.")
