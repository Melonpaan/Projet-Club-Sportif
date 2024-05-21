from personnel import Personnel

class Joueur(Personnel):
    def __init__(self, nom, prenom, date_naissance,poste, position, salaire, contrat):
        super().__init__(nom,prenom, date_naissance)
        self.poste = poste
        self.position = position
        self.salaire = salaire
        self.contrat = contrat
    
    

 