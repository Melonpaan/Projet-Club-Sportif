from classes.data_manager import DataManager

class Match:
    """
    Classe pour représenter un match de football.

    Attributs:
        date (str): La date du match.
        my_team (str): Le nom de mon équipe.
        opponent (str): Le nom de l'équipe adverse.
        players (list): La liste des joueurs participant au match.
    """

    def __init__(self, date, my_team, opponent, players=None):
        """
        Initialise un objet Match avec les informations fournies.

        Args:
            date (str): La date du match.
            my_team (str): Le nom de mon équipe.
            opponent (str): Le nom de l'équipe adverse.
            players (list, optionnel): La liste des joueurs participant au match. Par défaut, une liste vide.
        """
        self.date = date
        self.my_team = my_team
        self.opponent = opponent
        self.players = players if players else []

    def add_match(self, match_data, filename='data/matches.json'):
        """
        Ajoute un nouveau match aux données des matchs et sauvegarde dans un fichier JSON.

        Args:
            match_data (dict): Un dictionnaire contenant les données du match à ajouter.
            filename (str, optionnel): Le chemin du fichier JSON où les données des matchs sont sauvegardées. Par défaut, 'data/matches.json'.
        """
        matches = DataManager.load_from_file(filename) or []
        matches.append(match_data)
        DataManager.save_to_file(matches, filename)

    def add_team_to_match(self, team_data, filename='data/players.json'):
        """
        Ajoute une équipe de joueurs aux données d'un match et sauvegarde dans un fichier JSON.

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
