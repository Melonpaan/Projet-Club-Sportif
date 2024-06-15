from classes.person import Person
from classes.contract import Contract
from classes.data_manager import DataManager

class Staff(Person):
    last_id = 0
    available_ids = []

    def __init__(self, person_ID, last_name, first_name, birth_date, contract, address, phone_number, role, gender):
        """
        Initialise un objet Staff.

        Args:
            person_ID (int): ID du membre du personnel.
            last_name (str): Nom de famille du membre du personnel.
            first_name (str): Prénom du membre du personnel.
            birth_date (str): Date de naissance du membre du personnel.
            contract (Contract): Contrat du membre du personnel.
            address (str): Adresse du membre du personnel.
            phone_number (str): Numéro de téléphone du membre du personnel.
            role (str): Rôle du membre du personnel.
            gender (str): Genre du membre du personnel.
        """
        super().__init__(int(person_ID), last_name, first_name, birth_date, contract, address, phone_number, gender)
        self.role = role

        person_ID = int(person_ID)
        if person_ID > Staff.last_id:
            Staff.last_id = person_ID

    @classmethod
    def create_new(cls, last_name, first_name, birth_date, contract, address, phone_number, role, gender):
        """
        Crée un nouveau membre du personnel avec un ID unique.

        Args:
            last_name (str): Nom de famille du membre du personnel.
            first_name (str): Prénom du membre du personnel.
            birth_date (str): Date de naissance du membre du personnel.
            contract (Contract): Contrat du membre du personnel.
            address (str): Adresse du membre du personnel.
            phone_number (str): Numéro de téléphone du membre du personnel.
            role (str): Rôle du membre du personnel.
            gender (str): Genre du membre du personnel.

        Returns:
            Staff: Un nouvel objet Staff.
        """
        if cls.available_ids:
            new_id = cls.available_ids.pop(0)
        else:
            cls.last_id += 1
            new_id = cls.last_id
        return cls(new_id, last_name, first_name, birth_date, contract, address, phone_number, role, gender)

    @staticmethod
    def delete(staff):
        """
        Supprime un membre du personnel en ajoutant son ID à la liste des IDs disponibles.

        Args:
            staff (Staff): Le membre du personnel à supprimer.
        """
        Staff.available_ids.append(staff.person_ID)

    def update_details(self, last_name, first_name, birth_date, contract, address, phone_number, role, gender):
        """
        Met à jour les détails du membre du personnel.

        Args:
            last_name (str): Nom de famille du membre du personnel.
            first_name (str): Prénom du membre du personnel.
            birth_date (str): Date de naissance du membre du personnel.
            contract (Contract): Contrat du membre du personnel.
            address (str): Adresse du membre du personnel.
            phone_number (str): Numéro de téléphone du membre du personnel.
            role (str): Rôle du membre du personnel.
            gender (str): Genre du membre du personnel.
        """
        self.last_name = last_name
        self.first_name = first_name
        self.birth_date = birth_date
        self.contract.update(contract.start_date, contract.end_date, contract.salary)
        self.address = address
        self.phone_number = phone_number
        self.role = role
        self.gender = gender

    def to_dict(self):
        """
        Convertit les détails du membre du personnel en dictionnaire.

        Returns:
            dict: Détails du membre du personnel sous forme de dictionnaire.
        """
        data = super().to_dict()
        data.update({
            'role': self.role
        })
        return data

    @classmethod
    def from_dict(cls, data):
        """
        Crée un objet Staff à partir d'un dictionnaire.

        Args:
            data (dict): Dictionnaire contenant les détails du membre du personnel.

        Returns:
            Staff: Un objet Staff.
        """
        contract = Contract.from_dict(data['contract'])
        return cls(
            int(data['person_ID']), data['last_name'], data['first_name'],
            data['birth_date'], contract, data['address'], data['phone_number'],
            data['role'], data['gender']
        )

    @staticmethod
    def save_to_file(staff_members):
        """
        Sauvegarde la liste des membres du personnel dans un fichier JSON.

        Args:
            staff_members (list): Liste des objets Staff.
        """
        DataManager.save_to_file([staff.to_dict() for staff in staff_members], 'data/staff.json')

    @staticmethod
    def load_from_file():
        """
        Charge la liste des membres du personnel depuis un fichier JSON.

        Returns:
            list: Liste des objets Staff.
        """
        staff_data = DataManager.load_from_file('data/staff.json')
        staff_members = [Staff.from_dict(data) for data in staff_data]
        
        if staff_members:
            Staff.last_id = max(staff.person_ID for staff in staff_members)
        
        return staff_members
