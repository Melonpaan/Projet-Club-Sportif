from classes.data_manager import DataManager

class Team:
    last_id = 0
    available_ids = []

    def __init__(self, team_id, name, gender, category, players=None, doctor_id=None, coach_id=None):
        """
        Initialise un objet Team.

        Args:
            team_id (int): ID de l'équipe.
            name (str): Nom de l'équipe.
            gender (str): Genre de l'équipe.
            category (str): Catégorie de l'équipe.
            players (list): Liste des IDs des joueurs dans l'équipe.
            doctor_id (int): ID du docteur de l'équipe.
            coach_id (int): ID de l'entraîneur de l'équipe.
        """
        self.team_id = team_id
        self.name = name
        self.gender = gender
        self.category = category
        self.players = players if players is not None else []
        self.doctor_id = doctor_id
        self.coach_id = coach_id

        if team_id > Team.last_id:
            Team.last_id = team_id

    @classmethod
    def create_new(cls, name, gender, category, doctor_id=None, coach_id=None):
        """
        Crée une nouvelle équipe avec un ID unique.

        Args:
            name (str): Nom de l'équipe.
            gender (str): Genre de l'équipe.
            category (str): Catégorie de l'équipe.
            doctor_id (int): ID du docteur de l'équipe.
            coach_id (int): ID de l'entraîneur de l'équipe.

        Returns:
            Team: Un nouvel objet Team.
        """
        if cls.available_ids:
            new_id = cls.available_ids.pop(0)
        else:
            cls.last_id += 1
            new_id = cls.last_id
        return cls(new_id, name, gender, category, doctor_id, coach_id)

    @staticmethod
    def delete(team):
        """
        Supprime une équipe en ajoutant son ID à la liste des IDs disponibles.

        Args:
            team (Team): L'équipe à supprimer.
        """
        Team.available_ids.append(team.team_id)

    def update_details(self, name, gender, category, doctor_id=None, coach_id=None):
        """
        Met à jour les détails de l'équipe.

        Args:
            name (str): Nom de l'équipe.
            gender (str): Genre de l'équipe.
            category (str): Catégorie de l'équipe.
            doctor_id (int): ID du docteur de l'équipe.
            coach_id (int): ID de l'entraîneur de l'équipe.
        """
        self.name = name
        self.gender = gender
        self.category = category
        self.doctor_id = doctor_id
        self.coach_id = coach_id

    def add_player(self, player_id):
        """
        Ajoute un joueur à l'équipe.

        Args:
            player_id (int): ID du joueur à ajouter.
        """
        if not isinstance(self.players, list):
            self.players = []  
        if player_id not in self.players:
            self.players.append(player_id)
        
    def remove_player(self, player_id):
        """
        Supprime un joueur de l'équipe.

        Args:
            player_id (int): ID du joueur à supprimer.
        """
        if player_id in self.players:
            self.players.remove(player_id)

    def to_dict(self):
        """
        Convertit les détails de l'équipe en dictionnaire.

        Returns:
            dict: Détails de l'équipe sous forme de dictionnaire.
        """
        return {
            'team_id': self.team_id,
            'name': self.name,
            'gender': self.gender,
            'category': self.category,
            'players': self.players,
            'doctor_id': self.doctor_id,
            'coach_id': self.coach_id
        }

    @classmethod
    def from_dict(cls, data):
        """
        Crée un objet Team à partir d'un dictionnaire.

        Args:
            data (dict): Dictionnaire contenant les détails de l'équipe.

        Returns:
            Team: Un objet Team.
        """
        return cls(
            data['team_id'], data['name'], data['gender'], data['category'], data.get('players', []),
            data.get('doctor_id'), data.get('coach_id')
        )

    @staticmethod
    def save_to_file(teams):
        """
        Sauvegarde la liste des équipes dans un fichier JSON.

        Args:
            teams (list): Liste des objets Team.
        """
        DataManager.save_to_file([team.to_dict() for team in teams], 'data/teams.json')

    @staticmethod
    def load_from_file():
        """
        Charge la liste des équipes depuis un fichier JSON.

        Returns:
            list: Liste des objets Team.
        """
        teams_data = DataManager.load_from_file('data/teams.json')
        if teams_data is None:
            teams_data = []
        teams = [Team.from_dict(data) for data in teams_data]

        if teams:
            Team.last_id = max(team.team_id for team in teams)

        return teams