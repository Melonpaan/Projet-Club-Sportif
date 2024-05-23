from personnel import Personnel

class Joueur(Personnel):
    def __init__(self, nom, prenom, date_naissance,poste, position, salaire, contrat):
        super().__init__(nom,prenom, date_naissance)
        self.poste = poste
        self.position = position
        self.salaire = salaire
        self.contrat = contrat
    
    def to_dict(self):
        return {
            "nom": self.nom,
            "prenom": self.prenom,
            "date_naissance": self.date_naissance,
            "poste": self.poste,
            "position": self.position,
            "salaire": self.salaire,
            "contrat": self.contrat
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["nom"], data["prenom"], data["date_naissance"],
            data["poste"], data["position"], data["salaire"], data["contrat"]
        )
    

 