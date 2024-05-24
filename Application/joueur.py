import tkinter as tk
from personnel import Personnel
from data_manager import sauvegarder_donnees, charger_donnees

class Joueur(Personnel):
    def __init__(self, nom, prenom, date_naissance, poste, position, salaire, contrat):
        super().__init__(nom, prenom, date_naissance)
        self.poste = poste
        self.position = position
        self.salaire = salaire
        self.contrat = contrat

    def to_dict(self):
        return {
            "nom": self.nom,
            "prenom": self.prenom,
            "date_naissance": self.date_naissance,
            "poste": self.poste,
            "position": self.position,
            "salaire": self.salaire,
            "contrat": self.contrat
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["nom"], data["prenom"], data["date_naissance"],
            data["poste"], data["position"], data["salaire"], data["contrat"]
        )

    @staticmethod
    def ajouter_joueur(entries, joueurs, message_label):
        details = {label: entry.get() for label, entry in entries.items()}

        if not all(details.values()):
            message_label.config(text="Erreur: Tous les champs doivent être remplis", fg="red")
            message_label.pack()
            return

        if (details["Nom"], details["Prénom"]) in [(joueur.nom, joueur.prenom) for joueur in joueurs]:
            message_label.config(text="Erreur: Le joueur est déjà dans le club", fg="red")
            message_label.pack()
        else:
            nouveau_joueur = Joueur(
                details["Nom"], details["Prénom"], details["Date de naissance (JJ/MM/AAAA)"],
                details["Poste"], details["Position"], details["Salaire (€)"], details["Contrat (Durée)"]
            )
            joueurs.add(nouveau_joueur)
            Joueur.sauvegarder_joueurs("Application/data/joueurs.json", joueurs)
            message_label.config(text="Joueur ajouté avec succès", fg="green")
            message_label.pack()

        for entry in entries.values():
            entry.delete(0, tk.END)

    @staticmethod
    def supprimer_joueur(nom_entry, prenom_entry, joueurs, message_label):
        nom_joueur = nom_entry.get()
        prenom_joueur = prenom_entry.get()

        joueur_a_supprimer = None
        for joueur in joueurs:
            if joueur.nom == nom_joueur and joueur.prenom == prenom_joueur:
                joueur_a_supprimer = joueur
                break

        if joueur_a_supprimer:
            joueurs.remove(joueur_a_supprimer)
            Joueur.sauvegarder_joueurs("Application/data/joueurs.json", joueurs)
            message_label.config(text="Joueur supprimé avec succès", fg="green")
            message_label.pack()
        else:
            message_label.config(text="Erreur: Le joueur n'est pas dans le club", fg="red")
            message_label.pack()

        nom_entry.delete(0, tk.END)
        prenom_entry.delete(0, tk.END)

    @classmethod
    def sauvegarder_joueurs(cls, fichier_path, joueurs):
        joueurs_dict = [joueur.to_dict() for joueur in joueurs]
        sauvegarder_donnees(fichier_path, joueurs_dict)

    @classmethod
    def charger_joueurs(cls, fichier_path):
        joueurs_dict = charger_donnees(fichier_path)
        if joueurs_dict is None:
            return set()
        return {cls.from_dict(joueur) for joueur in joueurs_dict}
