import json
import os

def sauvegarder_donnees(fichier_path, donnees):
    """
    Sauvegarde les données dans un fichier JSON.

    Args:
        fichier_path (str): Chemin du fichier où les données seront sauvegardées.
        donnees (any): Données à sauvegarder (doit être sérialisable en JSON).
    """
    with open(fichier_path, "w") as fichier:
        json.dump(donnees, fichier)

def charger_donnees(fichier_path):
    """
    Charge les données depuis un fichier JSON.

    Args:
        fichier_path (str): Chemin du fichier à partir duquel les données seront chargées.

    Returns:
        any: Données chargées depuis le fichier, ou None si le fichier n'existe pas ou est vide.
    """
    if not os.path.exists(fichier_path):
        return None

    with open(fichier_path, "r") as fichier:
        try:
            return json.load(fichier)
        except json.JSONDecodeError:
            return None
