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
    
    def create_combobox(self, parent, label_text, row, values, default_value=None):
        Label(parent, text=label_text).grid(row=row, column=0)
        combobox = ttk.Combobox(parent, values=values)
        combobox.grid(row=row, column=1)
        if default_value:
            combobox.set(default_value)
        return combobox
    
     def open_form_widget(self, team=None):
        def submit():
            name = entry_name.get()
            genre = entry_genre.get()
            categorie = entry_categorie.get()

            if not name:
                messagebox.showerror("Erreur", "Le nom de l'équipe ne peut pas être vide.")
                return

            if team is None:
                new_team = Team.create_new(name, genre, categorie)
                self.gui_manager.teams.append(new_team)
                messagebox.showinfo("Information", f"Équipe ajoutée avec l'ID {new_team.team_id}")
            else:
                team.update_details(name, genre, categorie)
                messagebox.showinfo("Information", f"Équipe modifiée avec l'ID {team.team_id}")

            self.gui_manager.update_teams_treeview()
            Team.save_to_file(self.gui_manager.teams)
            form_window.destroy()

        form_window = Toplevel(self.gui_manager)
        form_window.title("Modifier une équipe" if team else "Ajouter une équipe")

        entry_name = self.create_form_widget(form_window, "Nom de l'équipe", 1, getattr(team, 'name', ''))
        entry_genre = self.create_combobox(form_window, "Genre", 2, ["Masculin", "Féminin"], getattr(team, 'genre', 'Genre'))
        entry_categorie = self.create_combobox(form_window, "Catégorie", 3,["Division 1","Division 2","Division 3","Division 4"], getattr(team, 'categorie', 'division'))

        Button(form_window, text="Modifier" if team else "Ajouter", command=submit).grid(row=4, column=0, columnspan=2)

    def add_team(self):
        self.open_form_widget()

    def modify_team(self):
        selected_item = self.gui_manager.tree_teams.selection()
        if selected_item:
            item = self.gui_manager.tree_teams.item(selected_item)
            values = item['values']
            team_id = int(values[0])
            team = next((team for team in self.gui_manager.teams if team.team_id == team_id), None)
            self.open_form_widget(team)
        else:
            messagebox.showerror("Erreur", "Aucune équipe sélectionnée")

    def delete_team(self):
        selected_item = self.gui_manager.tree_teams.selection()
        if selected_item:
            item = self.gui_manager.tree_teams.item(selected_item)
            values = item['values']
            team_id = int(values[0])
            team = next((team for team in self.gui_manager.teams if team.team_id == team_id), None)

            if team:
                confirmation = messagebox.askyesno("Confirmation", "Êtes-vous sûr de vouloir supprimer cette équipe ?")
                if confirmation:
                    Team.delete(team)
                    self.gui_manager.teams.remove(team)
                    self.gui_manager.update_teams_treeview()
                    Team.save_to_file(self.gui_manager.teams)
                    messagebox.showinfo("Équipe supprimée", "L'équipe a été supprimée avec succès.")
        else:
            messagebox.showerror("Erreur", "Aucune équipe sélectionnée")