from classes.data_manager import DataManager

class Match:
    """
    Classe pour représenter un match de football.
    """

    def __init__(self, match_id, date, my_team, opponent, players=None):
        """
        Initialise un objet Match avec les informations fournies.

        Args:
            match_id (int): L'ID du match.
            date (str): La date du match.
            my_team (str): Le nom de mon équipe.
            opponent (str): Le nom de l'équipe adverse.
            players (list, optionnel): La liste des joueurs participant au match. Par défaut, une liste vide.
        """
        self.match_id = match_id
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

