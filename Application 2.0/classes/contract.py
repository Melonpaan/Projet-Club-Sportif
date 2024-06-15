from datetime import datetime
from tkinter import messagebox
class Contract:
    """
    Classe représentant un contrat avec une date de début, une date de fin et un salaire.

    Attributs:
        start_date (str): La date de début du contrat au format JJ-MM-AAAA.
        end_date (str): La date de fin du contrat au format JJ-MM-AAAA.
        salary (str): Le salaire associé au contrat.

    Méthodes:
        __init__(start_date, end_date, salary): Initialise un nouveau contrat avec les dates et le salaire fournis.
        validate_date_format(date): Valide le format de la date fournie.
        update(start_date, end_date, salary): Met à jour les détails du contrat.
        to_dict(): Convertit les détails du contrat en dictionnaire.
        from_dict(data): Crée un objet Contract à partir d'un dictionnaire.
    """

    def __init__(self, start_date, end_date, salary):
        """
        Initialise un nouveau contrat avec les dates de début, de fin et le salaire fournis.
        
        Args:
            start_date (str): La date de début du contrat au format JJ-MM-AAAA.
            end_date (str): La date de fin du contrat au format JJ-MM-AAAA.
            salary (str): Le salaire associé au contrat.
        """
        self.start_date = start_date
        self.end_date = end_date
        self.salary = salary

        # Valider le format des dates
        self.validate_date_format(self.start_date)
        self.validate_date_format(self.end_date)
    
    def validate_date_format(self, date):
        """
        Valide que la date est au format JJ-MM-AAAA. Affiche un message d'erreur si le format est incorrect.

        Args:
            date (str): La date à valider.

        Returns:
            None
        """
        try:
            datetime.strptime(date, '%d-%m-%Y')
        except ValueError:
            return messagebox.showerror("Erreur", f"Le format de la date '{date}' doit être JJ-MM-AAAA")
        
    def update(self, start_date, end_date, salary):
        """
        Met à jour les détails du contrat.

        Args:
            start_date (str): La nouvelle date de début du contrat au format JJ-MM-AAAA.
            end_date (str): La nouvelle date de fin du contrat au format JJ-MM-AAAA.
            salary (str): Le nouveau salaire associé au contrat.

        Returns:
            None
        """
        self.start_date = start_date
        self.end_date = end_date
        self.salary = salary

        # Vérification des formats de dates
        self.validate_date_format(self.start_date)
        self.validate_date_format(self.end_date)

    def to_dict(self):
        """
        Convertit les détails du contrat en dictionnaire.

        Returns:
            dict: Un dictionnaire contenant les détails du contrat.
        """
        return {
            'start_date': self.start_date,
            'end_date': self.end_date,
            'salary': self.salary
        }

    @classmethod
    def from_dict(cls, data):
        """
        Crée un objet Contract à partir d'un dictionnaire.

        Args:
            data (dict): Un dictionnaire contenant les détails du contrat.

        Returns:
            Contract: Un objet Contract initialisé avec les données du dictionnaire.
        """
        return cls(data['start_date'], data['end_date'], data['salary'])