from datetime import date
from person import Person, Player, Staff
from team import Team
from club import Club
from transfer import Transfer
from training import Training
from match import Match, MatchResult, Sanction
from statistics_1 import PlayerStatistics
from stadium import Stadium
from season import Season


def main():

    # Création de personnes
    joueur1 = Player("John", "Doe", date(1990, 1, 1),
                     "Forward", 30, 50000, "Contract 2023")
    joueur2 = Player("Jane", "Smith", date(1992, 2, 2),
                     "Midfielder", 28, 60000, "Contract 2024")
    staff1 = Staff("Alice", "Johnson", date(1980, 3, 3),
                   "Coach", 70000, "Contract 2025")

    # Création d'une équipe
    equipe1 = Team("Team A")
    equipe1.add_player(joueur1, "2023")
    equipe1.add_staff(staff1, "2023")

    # Création d'un club
    club1 = Club("Club 1", "123 Main St")
    club1.add_player(joueur1)
    club1.add_player(joueur2)
    club1.add_staff(staff1)
    club1.add_team(equipe1)

    # Création d'un transfert
    transfert1 = Transfer(joueur1, club1, club1, date(2023, 6, 1), 1000000)
    club1.add_transfer(transfert1)

    # Création d'un stade
    stade1 = Stadium("Stadium 1", "456 Arena Rd", 50000)

    # Création d'un match
    match1 = Match(date(2023, 7, 1), stade1, equipe1, equipe1)
    match_result1 = MatchResult(equipe1, equipe1, 2, 1)
    match1.update_result(match_result1)

    # Création d'une saison
    saison1 = Season(2023)
    saison1.add_match_result(match_result1)
    saison1.add_transfer(transfert1)

    # Affichage des informations
    print(joueur1.display_info())
    print(staff1.display_info())

    print("Players in Team A for season 2023:")
    for player in equipe1.get_players_for_season("2023"):
        print(player.display_info())

    print("Transfers:")
    print(club1.display_transfers())

    print("Match Details:")
    print(match1.display_details())

    print("Stadium Details:")
    print(stade1.display_details())

    print("Match Results for Team A in season 2023:")
    for result in saison1.get_team_results(equipe1):
        print(result.display_result())


if __name__ == "__main__":
    main()
