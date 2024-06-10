from classes.data_manager import DataManager

class Training:
    """
    Classe pour représenter une séance d'entraînement de football.

    Attributs:
        date (str): La date de l'entraînement.
        my_team (str): Le nom de mon équipe.
        location (str): Le lieu de l'entraînement.
        players (list): La liste des joueurs participant à l'entraînement.
    """

    def __init__(self, date, my_team, location, players=None):
        """
        Initialise un objet Training avec les informations fournies.

        Args:
            date (str): La date de l'entraînement.
            my_team (str): Le nom de mon équipe.
            location (str): Le lieu de l'entraînement.
            players (list, optionnel): La liste des joueurs participant à l'entraînement. Par défaut, une liste vide.
        """
        self.date = date
        self.my_team = my_team
        self.location = location
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

    def add_team_to_training(self, team_data, filename='data/players.json'):
        """
        Ajoute une équipe de joueurs aux données d'un entraînement et sauvegarde dans un fichier JSON.

        Args:
            team_data (dict): Un dictionnaire contenant les données de l'équipe à ajouter.
            filename (str, optionnel): Le chemin du fichier JSON où les données des équipes sont sauvegardées. Par défaut, 'data/players.json'.

        Raises:
            FileNotFoundError: Si le fichier spécifié n'existe pas.
        """
        teams = DataManager.load_from_file(filename)
        if teams is not None:
            teams.append(team_data)
            DataManager.save_to_file(teams, filename)
        else:
            raise FileNotFoundError(f"The file {filename} does not exist.")
