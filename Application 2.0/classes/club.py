import json
import os

class Club:
    """
    Classe représentant un club de sport.

    Attributes:
        name (str): Le nom du club.
        address (str): L'adresse du club.
        president (str): Le nom du président du club.
        teams (list): Une liste des équipes associées au club.
    """

    def __init__(self, name, address, president):
        """
        Initialise une instance de la classe Club.

        Args:
            name (str): Le nom du club.
            address (str): L'adresse du club.
            president (str): Le nom du président du club.
        """
        self.name = name
        self.address = address
        self.president = president
        self.teams = []

    def to_dict(self):
        """
        Convertit l'instance du club en dictionnaire.

        Returns:
            dict: Un dictionnaire représentant les attributs du club.
        """
        return {
            'name': self.name,
            'address': self.address,
            'president': self.president,
            'teams': self.teams
        }

    @classmethod
    def from_dict(cls, data):
        """
        Crée une instance de la classe Club à partir d'un dictionnaire.

        Args:
            data (dict): Un dictionnaire contenant les données du club.

        Returns:
            Club: Une instance de la classe Club.
        """
        club = cls(data['name'], data['address'], data['president'])
        club.teams = data.get('teams', [])
        return club

    def save_to_file(self, filename='data/club.json'):
        """
        Sauvegarde les données du club dans un fichier JSON.

        Args:
            filename (str): Le chemin du fichier où sauvegarder les données. Par défaut 'data/club.json'.
        """
        folder = os.path.dirname(filename)
        if not os.path.exists(folder):
            os.makedirs(folder)
        with open(filename, 'w') as f:
            json.dump(self.to_dict(), f, indent=4)

    @classmethod
    def load_from_file(cls, filename='data/club.json'):
        """
        Charge les données du club à partir d'un fichier JSON.

        Args:
            filename (str): Le chemin du fichier à partir duquel charger les données. Par défaut 'data/club.json'.

        Returns:
            Club: Une instance de la classe Club avec les données chargées. Si le fichier n'existe pas, retourne une instance avec des valeurs par défaut.
        """
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                data = json.load(f)
                return cls.from_dict(data)
        return cls("Nom du Club", "Adresse du Club", "Président du Club")

