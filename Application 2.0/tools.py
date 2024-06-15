import tkinter as tk


class Tools:
    @staticmethod
    def create_button(parent, text, command, row, col, col_span=1):
        """
        Crée un bouton Tkinter et le place dans la grille.

        Args:
            parent: Widget parent.
            text (str): Texte du bouton.
            command (function): Commande à exécuter lors du clic sur le bouton.
            row (int): Ligne de la grille.
            col (int): Colonne de la grille.
            col_span (int): Nombre de colonnes à occuper.
        """
        button = tk.Button(parent, text=text, command=command)
        button.grid(row=row, column=col, columnspan=col_span, padx=5, pady=5, sticky=tk.W+tk.E)

    @staticmethod
    def create_label_and_entry(parent, label_text, row, default_value="", disabled=False):
        """
        Crée une étiquette et une entrée Tkinter, et les place dans la grille.

        Args:
            parent: Widget parent.
            label_text (str): Texte de l'étiquette.
            row (int): Ligne de la grille.
            default_value (str): Valeur par défaut de l'entrée.
            disabled (bool): Si vrai, désactive l'entrée.
        
        Returns:
            tk.Entry: Widget d'entrée.
        """
        label = tk.Label(parent, text=label_text)
        label.grid(row=row, column=0, sticky=tk.W, padx=5, pady=5)
        entry = tk.Entry(parent)
        entry.grid(row=row, column=1, padx=5, pady=5)
        entry.insert(0, default_value)
        if disabled:
            entry.config(state='disabled')
        return entry

    @staticmethod
    def create_label(parent, label_text, row, col, col_span=1):
        """
        Crée une étiquette Tkinter et la place dans la grille.

        Args:
            parent: Widget parent.
            label_text (str): Texte de l'étiquette.
            row (int): Ligne de la grille.
            col (int): Colonne de la grille.
            col_span (int): Nombre de colonnes à occuper.
        
        Returns:
            tk.Label: Widget étiquette.
        """
        label = tk.Label(parent, text=label_text)
        label.grid(row=row, column=col, columnspan=col_span, padx=5, pady=5, sticky=tk.W)
        return label

    @staticmethod
    def validate_entries(entries):
        """
        Valide les entrées du formulaire.

        Args:
            entries (dict): Dictionnaire des entrées à valider.

        Returns:
            bool: True si toutes les entrées sont valides, False sinon.
        """
        for key, entry in entries.items():
            if not entry.get():
                tk.messagebox.showerror("Erreur", f"{key} est obligatoire.")
                return False
        return True
