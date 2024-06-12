from classes.data_manager import DataManager
class Match:
    def __init__(self, match_id, date, my_team, opponent, players, score=None, statistics=None):
        self.match_id = match_id
        self.date = date
        self.my_team = my_team
        self.opponent = opponent
        self.players = players
        self.score = score
        self.statistics = statistics if statistics is not None else []

    def to_dict(self):
        return {
            "match_id": self.match_id,
            "date": self.date,
            "my_team": self.my_team,
            "opponent": self.opponent,
            "players": self.players,
            "score": self.score,
            "statistics": self.statistics
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            match_id=data["match_id"],
            date=data["date"],
            my_team=data["my_team"],
            opponent=data["opponent"],
            players=data["players"],
            score=data.get("score"),
            statistics=data.get("statistics", [])
        )

    def add_match(self, match_data):
        matches_data = DataManager.load_from_file('data/matches.json') or []
        matches_data.append(match_data)
        DataManager.save_to_file(matches_data, 'data/matches.json')
