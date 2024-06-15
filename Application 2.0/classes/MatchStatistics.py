from data_manager import DataManager

class MatchStatistics:
    """
    Classe représentant les statistiques d'un match.

    Attributs:
        match_id (int): L'identifiant unique du match.
        score (str): Le score du match.
        goals (list): Une liste des buts marqués dans le match.
        fouls (list): Une liste des fautes commises dans le match.

    Méthodes:
        __init__(match_id, score, goals, fouls): Initialise les statistiques d'un match.
        record_statistics(statistics_data, filename='statistics.json'): Enregistre les statistiques dans un fichier JSON.
    """

    def __init__(self, match_id, score, goals, fouls):
        """
        Initialise les statistiques d'un match.

        Args:
            match_id (int): L'identifiant unique du match.
            score (str): Le score du match.
            goals (list): Une liste des buts marqués dans le match.
            fouls (list): Une liste des fautes commises dans le match.
        """
        self.match_id = match_id
        self.score = score
        self.goals = goals
        self.fouls = fouls

    def record_statistics(self, statistics_data, filename='statistics.json'):
        """
        Enregistre les statistiques du match dans un fichier JSON.

        Args:
            statistics_data (dict): Les données statistiques à enregistrer.
            filename (str, optionnel): Le nom du fichier JSON où les statistiques seront enregistrées. 
                                       Par défaut, 'statistics.json'.

        Returns:
            None
        """
        statistics = DataManager.load_from_file(filename) or []
        statistics.append(statistics_data)
        DataManager.save_to_file(statistics, filename)
