from tkinter import Toplevel, Label, Entry, Button, messagebox, ttk
from classes.team import Team

class TeamPage:
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