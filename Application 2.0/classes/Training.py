from classes.data_manager import DataManager

class Training:
    """
    Classe pour représenter un entraînement de football.

    Attributs:
        training_id (int): L'ID unique de l'entraînement.
        date (str): La date de l'entraînement.
        my_team (str): Le nom de mon équipe.
        location (str): Le lieu de l'entraînement.
        training_type (str): Le type d'entraînement.
        players (list): La liste des joueurs participant à l'entraînement.
    """

    def __init__(self, training_id, date, my_team, location, training_type, players=None):
        """
        Initialise un objet Training avec les informations fournies.

        Args:
            training_id (int): L'ID unique de l'entraînement.
            date (str): La date de l'entraînement.
            my_team (str): Le nom de mon équipe.
            location (str): Le lieu de l'entraînement.
            training_type (str): Le type d'entraînement.
            players (list, optionnel): La liste des joueurs participant à l'entraînement. Par défaut, une liste vide.
        """
        self.training_id = training_id
        self.date = date
        self.my_team = my_team
        self.location = location
        self.training_type = training_type
        self.players = players if players else []

    def add_training(self, training_data, filename='data/trainings.json'):
        """
        Ajoute un nouvel entraînement aux données des entraînements et sauvegarde dans un fichier JSON.

        Args:
            training_data (dict): Un dictionnaire contenant les données de l'entraînement à ajouter.
            filename (str, optionnel): Le chemin du fichier JSON où les données des entraînements sont sauvegardées. Par défaut, 'data/trainings.json'.
        """
        trainings = DataManager.load_from_file(filename) or []
        trainings.append(training_data)
        DataManager.save_to_file(trainings, filename)


