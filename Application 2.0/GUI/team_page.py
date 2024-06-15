import tkinter as tk
from tkinter import Toplevel, Label, Button, Entry, ttk, messagebox
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
            gender = entry_gender.get()
            category = entry_category.get()
            doctor_id = int(entry_doctor.get().split()[-1][:-1]) if entry_doctor.get() else None
            coach_id = int(entry_coach.get().split()[-1][:-1]) if entry_coach.get() else None

            if not name:
                messagebox.showerror("Erreur", "Le nom de l'équipe ne peut pas être vide.")
                return

            if team is None:
                new_team = Team.create_new(name, gender, category, doctor_id, coach_id)
                self.gui_manager.teams.append(new_team)
                messagebox.showinfo("Information", f"Équipe ajoutée avec l'ID {new_team.team_id}")
            else:
                team.update_details(name, gender, category, doctor_id, coach_id)
                messagebox.showinfo("Information", f"Équipe modifiée avec l'ID {team.team_id}")

            self.gui_manager.update_teams_treeview()
            Team.save_to_file(self.gui_manager.teams)
            form_window.destroy()

        form_window = Toplevel(self.gui_manager)
        form_window.title("Modifier une équipe" if team else "Ajouter une équipe")

        entry_name = self.create_form_widget(form_window, "Nom de l'équipe", 1, getattr(team, 'name', ''))
        entry_gender = self.create_combobox(form_window, "Genre", 2, ["Masculin", "Féminin"], getattr(team, 'gender', ''))
        entry_category = self.create_combobox(form_window, "Catégorie", 3, ["Division 1", "Division 2", "Division 3", "Division 4"], getattr(team, 'category', ''))
        
        # Combobox pour le médecin et l'entraîneur
        doctor_values = [f"{staff.first_name} {staff.last_name} (ID: {staff.person_ID})" for staff in self.gui_manager.staff_members if staff.role == "Médecin"]
        coach_values = [f"{staff.first_name} {staff.last_name} (ID: {staff.person_ID})" for staff in self.gui_manager.staff_members if staff.role == "Entraîneur"]
        entry_doctor = self.create_combobox(form_window, "Médecin", 4, doctor_values, self.gui_manager.get_staff_name_by_id(getattr(team, 'doctor_id', None)))
        entry_coach = self.create_combobox(form_window, "Entraîneur", 5, coach_values, self.gui_manager.get_staff_name_by_id(getattr(team, 'coach_id', None)))

        Button(form_window, text="Modifier" if team else "Ajouter", command=submit).grid(row=6, column=0, columnspan=2)

    def add_team(self):
        self.open_form_widget()

    def modify_team(self):
        selected_item = self.gui_manager.tree_teams.selection()
        if selected_item:
            item = self.gui_manager.tree_teams.item(selected_item)
            values = item['values']
            team_id = str(values[0])
            team = None
            for data in self.gui_manager.teams:
                if str(data.team_id) == team_id:
                    team = data
                    break
            self.open_form_widget(team)
        else:
            messagebox.showerror("Erreur", "Aucune équipe sélectionnée")

    def delete_team(self):
        selected_item = self.gui_manager.tree_teams.selection()
        if selected_item:
            item = self.gui_manager.tree_teams.item(selected_item)
            values = item['values']
            team_id = str(values[0])
            team = None
            for data in self.gui_manager.teams:
                if str(data.team_id) == team_id:
                    team = data
                    break

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

    def add_players_to_team(self):
        """
        Ouvre une fenêtre pour sélectionner et ajouter des joueurs à l'équipe sélectionnée.
        """
        selected_item = self.gui_manager.tree_teams.selection()
        if selected_item:
            item = self.gui_manager.tree_teams.item(selected_item)
            team_id = item['values'][0]
            team = None
            for data in self.gui_manager.teams:
                if data.team_id == team_id:
                    team = data
                    break

            if team:
                self.open_add_players_window(team)
            else:
                messagebox.showerror("Erreur", "Équipe non trouvée")
        else:
            messagebox.showerror("Erreur", "Aucune équipe sélectionnée")

    def open_add_players_window(self, team):
        """
        Ouvre une fenêtre pour sélectionner et ajouter des joueurs à une équipe.
        """
        add_players_window = Toplevel(self.gui_manager)
        add_players_window.title(f"Ajouter des joueurs à l'équipe {team.name}")

        players_tree = ttk.Treeview(add_players_window, columns=("Nom", "Prénom", "Poste", "Équipe"), selectmode='extended')
        players_tree.heading("#0", text="ID")
        players_tree.heading("Nom", text="Nom")
        players_tree.heading("Prénom", text="Prénom")
        players_tree.heading("Poste", text="Poste")
        players_tree.heading("Équipe", text="Équipe")
        players_tree.pack(fill=tk.BOTH, expand=True)

        for player in self.gui_manager.players:
            if player.gender == team.gender:
                team_name = self.get_player_team(player.person_ID)
                players_tree.insert("", "end", text=player.person_ID, values=(player.last_name, player.first_name, player.position, team_name or ""))

        def add_selected_players():
            selected_items = players_tree.selection()
            for item in selected_items:
                player_id = int(players_tree.item(item, "text"))
                current_team_name = self.get_player_team(player_id)
                if current_team_name and current_team_name != team.name:
                    confirmation = messagebox.askyesno("Confirmation",f"Le joueur est déja dans l'équipe {current_team_name}. Voulez-vous le déplacer dans l'équipe {team.name} ?")
                    if confirmation:
                        for _ in self.gui_manager.teams:
                            if player_id in _.players:
                                _.players.remove(player_id)
                team.add_player(player_id)

            self.gui_manager.update_teams_treeview()
            Team.save_to_file(self.gui_manager.teams)
            add_players_window.destroy()

        add_button = Button(add_players_window, text="Ajouter", command=add_selected_players)
        add_button.pack()

    def view_team_players(self):
        """
        Ouvre une fenêtre pour afficher les joueurs d'une équipe sélectionnée.
        """
        selected_item = self.gui_manager.tree_teams.selection()
        if selected_item:
            item = self.gui_manager.tree_teams.item(selected_item)
            team_id = item['values'][0]
            team = None
            for data in self.gui_manager.teams:
                if data.team_id == team_id:
                    team = data
                    break

            if team:
                self.open_view_team_players_window(team)
            else:
                messagebox.showerror("Erreur", "Équipe non trouvée")
        else:
            messagebox.showerror("Erreur", "Aucune équipe sélectionnée")

    def open_view_team_players_window(self, team):
        """
        Ouvre une fenêtre pour afficher les joueurs d'une équipe.
        """
        view_players_window = Toplevel(self.gui_manager)
        view_players_window.title(f"Joueurs de l'équipe {team.name}")

        players_tree = ttk.Treeview(view_players_window, columns=("Nom", "Prénom", "Poste"))
        players_tree.heading("#0", text="ID")
        players_tree.heading("Nom", text="Nom")
        players_tree.heading("Prénom", text="Prénom")
        players_tree.heading("Poste", text="Poste")
        players_tree.pack(fill=tk.BOTH, expand=True)

        for player_id in team.players:
            player = None
            for p in self.gui_manager.players:
                if p.person_ID == player_id:
                    player = p
                    break
            if player:
                players_tree.insert("", "end", text=player.person_ID, values=(player.last_name, player.first_name, player.position))

        def remove_selected_player():
            selected_item = players_tree.selection()
            if selected_item:
                player_id = int(players_tree.item(selected_item, "text"))
                confirmation = messagebox.askyesno("Confirmation", f"Voulez-vous vraiment supprimer ce joueur de l'équipe {team.name} ?")
                if confirmation:
                    team.players.remove(player_id)
                    self.gui_manager.update_teams_treeview()
                    Team.save_to_file(self.gui_manager.teams)
                    players_tree.delete(selected_item)
                    messagebox.showinfo("Succès", "Le joueur a été supprimé de l'équipe avec succès.")
            else:
                messagebox.showerror("Erreur", "Aucun joueur sélectionné")

        remove_button = Button(view_players_window, text="Supprimer Joueur", command=remove_selected_player)
        remove_button.pack()

        close_button = Button(view_players_window, text="Fermer", command=view_players_window.destroy)
        close_button.pack()
    def get_player_team(self, player_id):
        """
        Retourne le nom de l'équipe à laquelle appartient le joueur.
        """
        for team in self.gui_manager.teams:
            if player_id in team.players:
                return team.name
        return None

    