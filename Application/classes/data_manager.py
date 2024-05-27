import json
import os

class DataManager:
    @staticmethod
    def save_to_file(data, filename):
        # Vérifier si le dossier existe, sinon le créer
        folder = os.path.dirname(filename)
        if not os.path.exists(folder):
            os.makedirs(folder)

        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)

    @staticmethod
    def load_from_file(filename):
        try:
            with open(filename, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []
