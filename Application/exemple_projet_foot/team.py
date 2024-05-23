class Team:
    def __init__(self, team_name):
        self.team_name = team_name
        self.players_by_season = {}
        self.staff_by_season = {}

    def add_player(self, player, season):
        if season not in self.players_by_season:
            self.players_by_season[season] = []
        if player in self.players_by_season[season]:
            print(f"{player.first_name} {
                  player.last_name} is already in the team for season {season}.")
        else:
            self.players_by_season[season].append(player)
            player.assign_team(self, season)

    def remove_player(self, player, season):
        if season in self.players_by_season and player in self.players_by_season[season]:
            self.players_by_season[season].remove(player)

    def add_staff(self, staff, season):
        if season not in self.staff_by_season:
            self.staff_by_season[season] = []
        if staff in self.staff_by_season[season]:
            print(f"{staff.first_name} {
                  staff.last_name} is already in the team for season {season}.")
        else:
            self.staff_by_season[season].append(staff)

    def remove_staff(self, staff, season):
        if season in self.staff_by_season and staff in self.staff_by_season[season]:
            self.staff_by_season[season].remove(staff)

    def get_players_for_season(self, season):
        return self.players_by_season.get(season, [])

    def get_staff_for_season(self, season):
        return self.staff_by_season.get(season, [])

    def __str__(self):
        return f"Team Name: {self.team_name}"
