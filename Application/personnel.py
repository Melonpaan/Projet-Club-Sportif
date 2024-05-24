class Personnel:
    def __init__(self, nom, prenom, date_naissance):
        self.nom = nom
        self.prenom = prenom
        self.date_naissance = date_naissance
        #self.salaire = salaire
        #self.contrat = contrat


    def __str__(self):
        return f"{self.nom} {self.prenom},Né le:{self.date_naissance} "

    def calculate_total_salaries(self):
        pass
    def update_contract(self):
        pass
    def display_info(self):
        pass
    