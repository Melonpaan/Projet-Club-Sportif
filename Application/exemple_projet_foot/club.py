class Club:
    def __init__(self, name, address):
        self.name = name
        self.address = address
        self.players = []
        self.staff = []
        self.teams = []
        self.transfers = []
        self.seasons = []

    def add_player(self, player):
        player.club = self
        self.players.append(player)

    def remove_player(self, player):
        if player in self.players:
            player.club = None
            self.players.remove(player)

    def add_staff(self, staff):
        staff.club = self
        self.staff.append(staff)

    def remove_staff(self, staff):
        if staff in self.staff:
            staff.club = None
            self.staff.remove(staff)

    def add_team(self, team):
        self.teams.append(team)

    def remove_team(self, team):
        if team in self.teams:
            self.teams.remove(team)

    def add_transfer(self, transfer):
        self.transfers.append(transfer)

    def add_season(self, season):
        if season not in self.seasons:
            self.seasons.append(season)
        else:
            print(f"Season {season.year} already exists.")

    def get_season(self, year):
        for season in self.seasons:
            if season.year == year:
                return season
        return None

    def display_transfers(self):
        return "\n".join([transfer.display_details() for transfer in self.transfers])

    def __str__(self):
        return f"Club Name: {self.name}, Address: {self.address}, Players: {len(self.players)}, Staff: {len(self.staff)}"
