from datetime import date


class Person:
    def __init__(self, first_name, last_name, birth_date, salary, contract_details):
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.salary = salary
        self.contract_details = contract_details

    def calculate_total_salaries(self):
        return self.salary

    def update_contract(self, new_contract_details):
        self.contract_details = new_contract_details

    def display_info(self):
        return (f"Name: {self.first_name} {self.last_name}, Birth Date: {self.birth_date}, Salary: {self.salary}, "
                f"Contract: {self.contract_details}")

    def __str__(self):
        return self.display_info()


class Player(Person):
    def __init__(self, first_name, last_name, birth_date, position, age, salary, contract_details, club=None):
        super().__init__(first_name, last_name, birth_date, salary, contract_details)
        self.position = position
        self.age = age
        self.club = club
        self.teams_by_season = {}

    def assign_team(self, team, season):
        self.teams_by_season[season] = team

    def get_team_for_season(self, season):
        return self.teams_by_season.get(season, None)

    def calculate_total_salaries(self):
        return self.salary

    def __str__(self):
        return self.display_info()


class Staff(Person):
    def __init__(self, first_name, last_name, birth_date, role, salary, contract_details, club=None):
        super().__init__(first_name, last_name, birth_date, salary, contract_details)
        self.role = role
        self.club = club

    def calculate_total_salaries(self):
        return self.salary

    def __str__(self):
        return self.display_info()
