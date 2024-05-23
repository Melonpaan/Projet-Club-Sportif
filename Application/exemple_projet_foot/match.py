# Classe match

class Match:
    def __init__(self, date, stadium, home_team, away_team):
        self.date = date
        self.stadium = stadium
        self.home_team = home_team
        self.away_team = away_team
        self.match_result = None
        self.player_statistics = []  
        self.sanctions = []  

    def add_player_statistics(self, player_statistics):
        self.player_statistics.append(player_statistics)

    def add_sanction(self, sanction):
        self.sanctions.append(sanction)

    def update_result(self, match_result):
        self.match_result = match_result

    def display_details(self):
        details = f"Match on {self.date} at {self.stadium.name}\n" \
            f"Teams: {self.home_team.team_name} vs {self.away_team.team_name}\n" \
            f"Result: {self.match_result.display_result() if self.match_result else 'Not available'}\n" \
            f"Player Statistics: {len(self.player_statistics)} entries\n" \
            f"Sanctions: {len(self.sanctions)} entries"
        return details

    def __str__(self):
        return self.display_details()

# Classe résultats


class MatchResult:
    def __init__(self, home_team, away_team, home_team_score, away_team_score):
        self.home_team = home_team
        self.away_team = away_team
        self.home_team_score = home_team_score
        self.away_team_score = away_team_score

    def calculate_winner(self):
        if self.home_team_score > self.away_team_score:
            return self.home_team
        elif self.home_team_score < self.away_team_score:
            return self.away_team
        else:
            return None  # Draw

    def display_result(self):
        winner = self.calculate_winner()
        if winner:
            result = f"{self.home_team.team_name} {self.home_team_score} - {self.away_team_score} {self.away_team.team_name}\n" \
                f"Winner: {winner.team_name}"
        else:
            result = f"{self.home_team.team_name} {self.home_team_score} - {self.away_team_score} {self.away_team.team_name}\n" \
                f"Result: Draw"
        return result

    def __str__(self):
        return self.display_details()

# Classe sanctions


class Sanction:
    def __init__(self, player, sanction_type, minute):
        self.player = player
        self.sanction_type = sanction_type  # 'Yellow Card' or 'Red Card'
        self.minute = minute

    def display_details(self):
        return f"{self.sanction_type} for {self.player.first_name} {self.player.last_name} at {self.minute} minute"
