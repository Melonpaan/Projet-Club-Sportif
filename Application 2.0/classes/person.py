from classes.contract import Contract

class Person:
    """
    Classe représentant une personne avec des attributs communs.

    Attributs:
        person_ID (int): L'identifiant unique de la personne.
        last_name (str): Le nom de famille de la personne.
        first_name (str): Le prénom de la personne.
        birth_date (str): La date de naissance de la personne au format JJ-MM-AAAA.
        contract (Contract): Le contrat associé à la personne.
        address (str): L'adresse de la personne.
        phone_number (str): Le numéro de téléphone de la personne.
        gender (str): Le genre de la personne.

    Méthodes:
        __init__(person_ID, last_name, first_name, birth_date, contract, address, phone_number, gender): Initialise une nouvelle instance de la classe Person.
        to_dict(): Convertit les informations de la personne en un dictionnaire.
        from_dict(data): Crée une instance de Person à partir d'un dictionnaire de données.
    """

    def __init__(self, person_ID, last_name, first_name, birth_date, contract, address, phone_number, gender):
        """
        Initialise une nouvelle instance de la classe Person.

        Args:
            person_ID (int): L'identifiant unique de la personne.
            last_name (str): Le nom de famille de la personne.
            first_name (str): Le prénom de la personne.
            birth_date (str): La date de naissance de la personne au format JJ-MM-AAAA.
            contract (Contract): Le contrat associé à la personne.
            address (str): L'adresse de la personne.
            phone_number (str): Le numéro de téléphone de la personne.
            gender (str): Le genre de la personne.
        """
        self.person_ID = person_ID
        self.last_name = last_name
        self.first_name = first_name
        self.birth_date = birth_date
        self.contract = contract  
        self.address = address
        self.phone_number = phone_number
        self.gender = gender

    def to_dict(self):
        """
        Convertit les informations de la personne en un dictionnaire.

        Returns:
            dict: Un dictionnaire contenant les informations de la personne.
        """
        return {
            'person_ID': self.person_ID,
            'last_name': self.last_name,
            'first_name': self.first_name,
            'birth_date': self.birth_date,
            'contract': self.contract.to_dict(),  
            'address': self.address,
            'phone_number': self.phone_number,
            'gender': self.gender
        }

    @classmethod
    def from_dict(cls, data):
        """
        Crée une instance de Person à partir d'un dictionnaire de données.

        Args:
            data (dict): Un dictionnaire contenant les données pour créer une instance de Person.

        Returns:
            Person: Une instance de la classe Person.
        """
        contract = Contract.from_dict(data['contract'])  
        return cls(
            data['person_ID'],
            data['last_name'],
            data['first_name'],
            data['birth_date'],
            contract,  
            data['address'],
            data['phone_number'],
            data['gender']
        )
