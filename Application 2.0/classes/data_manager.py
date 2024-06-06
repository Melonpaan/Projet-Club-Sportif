import json
import os

class DataManager:
    """
    Classe DataManager pour gérer les opérations de chargement et de sauvegarde des données.
    """

    @staticmethod
    def save_to_file(data, filename):
        """
        Sauvegarde les données dans un fichier JSON.

        Args:
            data (any): Les données à sauvegarder.
            filename (str): Le chemin du fichier JSON où sauvegarder les données.
        """
        # Vérifier si le dossier existe, sinon le créer
        folder = os.path.dirname(filename)
        if not os.path.exists(folder):
            os.makedirs(folder)

        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)

    @staticmethod
    def load_from_file(filename):
        """
        Charge les données à partir d'un fichier JSON.

        Args:
            filename (str): Le chemin du fichier JSON à partir duquel charger les données.

        Returns:
            any: Les données chargées à partir du fichier JSON. Retourne une liste vide si le fichier n'existe pas.
        """
        try:
            if os.path.exists(filename):
                with open(filename, 'r') as f:
                    return json.load(f)
            else:
                return None
        except FileNotFoundError:
            return None

