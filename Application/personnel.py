class Personnel:
    def __init__(self, nom, prenom, date_naissance):
        self.nom = nom
        self.prenom = prenom
        self.date_naissance = date_naissance


    def __str__(self):
        return f"{self.nom} {self.prenom},Né le:{self.date_naissance} "
