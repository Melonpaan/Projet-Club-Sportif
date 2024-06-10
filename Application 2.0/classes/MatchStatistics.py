from data_manager import DataManager

class MatchStatistics:
    def __init__(self, match_id, score, goals, fouls):
        self.match_id = match_id
        self.score = score
        self.goals = goals
        self.fouls = fouls

    def record_statistics(self, statistics_data, filename='statistics.json'):
        statistics = DataManager.load_from_file(filename) or []
        statistics.append(statistics_data)
        DataManager.save_to_file(statistics, filename)
