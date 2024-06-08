import tkinter as tk


class Tools:
    @staticmethod
    def create_button(parent, text, command, row, col, col_span=1):
        """
        Crée un bouton Tkinter et le place dans la grille.

        :param parent: Widget parent.
        :param text: Texte du bouton.
        :param command: Commande à exécuter lors du clic sur le bouton.
        :param row: Ligne de la grille.
        :param col: Colonne de la grille.
        :param col_span: Nombre de colonnes à occuper.
        """
        button = tk.Button(parent, text=text, command=command)
        button.grid(row=row, column=col, columnspan=col_span,
                    padx=5, pady=5, sticky=tk.W+tk.E)

    @staticmethod
    def create_label_and_entry(parent, label_text, row, default_value="", disabled=False):
        """
        Crée une étiquette et une entrée Tkinter, et les place dans la grille.

        :param parent: Widget parent.
        :param label_text: Texte de l'étiquette.
        :param row: Ligne de la grille.
        :param default_value: Valeur par défaut de l'entrée.
        :param disabled: Si vrai, désactive l'entrée.
        :return: Widget d'entrée.
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

        :param parent: Widget parent.
        :param label_text: Texte de l'étiquette.
        :param row: Ligne de la grille.
        :param col: Colonne de la grille.
        :param col_span: Nombre de colonnes à occuper.
        :return: Widget étiquette.
        """
        label = tk.Label(parent, text=label_text)
        label.grid(row=row, column=col, columnspan=col_span,
                   padx=5, pady=5, sticky=tk.W)
        return label

    @staticmethod
    def validate_entries(entries):
        """
        Valide les entrées du formulaire.

        :param entries: Dictionnaire des entrées à valider.
        :return: True si toutes les entrées sont valides, False sinon.
        """
        for key, entry in entries.items():
            if not entry.get():
                tk.messagebox.showerror("Erreur", f"{key} est obligatoire.")
                return False
        return True
