class PlayerStatistics:
    def __init__(self, player):
        self.player = player
        self.goals = 0
        self.assists = 0
        self.minutes_played = 0
        self.shots = 0
        self.fouls = 0

    def update_statistics(self, goals=0, assists=0, minutes_played=0, shots=0, fouls=0):
        self.goals += goals
        self.assists += assists
        self.minutes_played += minutes_played
        self.shots += shots
        self.fouls += fouls

    def display_statistics(self):
        stats = f"Statistics for {self.player.first_name} {self.player.last_name}:\n" \
                f"Goals: {self.goals}\n" \
                f"Assists: {self.assists}\n" \
                f"Minutes Played: {self.minutes_played}\n" \
                f"Shots: {self.shots}\n" \
                f"Fouls: {self.fouls}"
        return stats
