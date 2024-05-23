class Transfer:
    def __init__(self, player, from_club, to_club, transfer_date, transfer_fee):
        self.player = player
        self.from_club = from_club
        self.to_club = to_club
        self.transfer_date = transfer_date
        self.transfer_fee = transfer_fee

    def display_details(self):
        return f"Transfer Details:\n" \
            f"Player: {self.player.first_name} {self.player.last_name}\n" \
            f"From: {self.from_club.name}\n" \
            f"To: {self.to_club.name}\n" \
            f"Date: {self.transfer_date}\n" \
            f"Fee: {self.transfer_fee}"

    def __str__(self):
        return self.display_details()
