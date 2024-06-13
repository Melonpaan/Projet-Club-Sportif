from classes.data_manager import DataManager

class Match:
    """
    Classe pour représenter un match de football.
    """

    def __init__(self, match_id, date, my_team, opponent, players, score=None, statistics=None, yellow_cards=None, red_cards=None):
        """
        Initialise un objet Match avec les informations fournies.

        Args:
            match_id (int): L'ID unique du match.
            date (str): La date du match.
            my_team (str): Le nom de mon équipe.
            opponent (str): Le nom de l'équipe adverse.
            players (list): La liste des joueurs participant au match.
            score (str, optionnel): Le score du match.
            statistics (list, optionnel): Les statistiques du match (buteurs, passeurs, minutes).
            yellow_cards (list, optionnel): Les joueurs ayant reçu des cartons jaunes.
            red_cards (list, optionnel): Les joueurs ayant reçu des cartons rouges.
        """
        self.match_id = match_id
        self.date = date
        self.my_team = my_team
        self.opponent = opponent
        self.players = players
        self.score = score
        self.statistics = statistics if statistics else []
        self.yellow_cards = yellow_cards if yellow_cards else []
        self.red_cards = red_cards if red_cards else []

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

    @classmethod
    def from_dict(cls, data):
        """
        Crée un objet Match à partir d'un dictionnaire.

        Args:
            data (dict): Les données du match sous forme de dictionnaire.

        Returns:
            Match: Un objet Match.
        """
        return cls(
            data['match_id'],
            data['date'],
            data['my_team'],
            data['opponent'],
            data['players'],
            data.get('score'),
            data.get('statistics'),
            data.get('yellow_cards'),
            data.get('red_cards')
        )

    def to_dict(self):
        """
        Convertit l'objet Match en dictionnaire.

        Returns:
            dict: Les données du match sous forme de dictionnaire.
        """
        return {
            'match_id': self.match_id,
            'date': self.date,
            'my_team': self.my_team,
            'opponent': self.opponent,
            'players': self.players,
            'score': self.score,
            'statistics': self.statistics,
            'yellow_cards': self.yellow_cards,
            'red_cards': self.red_cards
        }
