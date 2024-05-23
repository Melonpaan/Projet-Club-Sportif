# Classe Saison

class Season:
    def __init__(self, year):
        self.year = year
        self.match_results = []  # List of MatchResult
        self.transfers = []  # List of Transfer

    def add_match_result(self, match_result):
        self.match_results.append(match_result)

    def add_transfer(self, transfer):
        self.transfers.append(transfer)

    def get_team_results(self, team):
        return [result for result in self.match_results if result.home_team == team or result.away_team == team]

    def get_player_transfers(self, player):
        return [transfer for transfer in self.transfers if transfer.player == player]

    def get_player_statistics(self, player):
        stats = []
        for match_result in self.match_results:
            for stat in match_result.match.player_statistics:
                if stat.player == player:
                    stats.append(stat)
        return stats

    def get_salary_expenses(self):
        salary_expenses = 0
        for transfer in self.transfers:
            salary_expenses += transfer.player.salary
        return salary_expenses