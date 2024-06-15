# Gestion de Club de Football

Ce projet est une application de gestion de club de football permettant de gérer les joueurs, les matchs, les entraînements, et bien plus encore.

## Fonctionnalités

- Gestion des joueurs : ajout, modification, suppression, et visualisation des joueurs.
- Gestion du staff : ajout, modification, suppression, et visualisation du staff.
- Gestion des équipes : ajout, modification, suppression, et visualisation des équipes.
- Gestion des matchs : ajout, modification, suppression, et visualisation des matchs.
- Gestion des entraînements : ajout, modification, suppression, et visualisation des entraînements.
- Statistiques des joueurs : visualisation des buts, passes décisives, cartons jaunes et rouges des joueurs.

## Prérequis

- Python 3.8 ou plus récent
- Tkinter (inclus dans la plupart des distributions Python)
- git (pour cloner le projet)

## Installation

### 1. Cloner le dépôt

git clone https://github.com/Melonpaan/Projet-Club-Sportif
cd <NOM_DU_REPERTOIRE_CLONE>

## 2. Créer un environnement virtuel

python -m venv venv

## 3. Activer l'environnement virtuel
  **Sur Windows :**
  
  - venv\Scripts\activate

  **Sur macOS et Linux :**

  - source venv/bin/activate
  
## 4. Exécuter l'application

python main.py

## Structure du Projet

- **`main.py`** : Point d'entrée de l'application.
- **`GUI/`** : Contient les fichiers pour l'interface graphique.
  - **`interface.py`** : Gère la fenêtre principale et les différents onglets.
  - **`player_page.py`** : Gère la page des joueurs.
  - **`staff_page.py`** : Gère la page du staff.
  - **`season_page.py`** : Gère la page des saisons.
  - **`team_page.py`** : Gère la page des équipes.
  - **`match_page.py`** : Gère la page des matchs.
  - **`training_page.py`** : Gère la page des entraînements.
  - **`statistics_page.py`** : Gère la page des statistiques.
- **`classes/`** : Contient les classes principales utilisées dans l'application.
  - **`player.py`** : Classe pour les joueurs.
  - **`staff.py`** : Classe pour le staff.
  - **`club.py`** : Classe pour le club.
  - **`team.py`** : Classe pour les équipes.
  - **`match.py`** : Classe pour les matchs.
  - **`training.py`** : Classe pour les entraînements.
  - **`contract.py`** : Classe pour les contrats, gérant les informations contractuelles des joueurs et du staff.
  - **`person.py`** : Classe de base pour les personnes (joueurs et staff), incluant les informations personnelles et contractuelles.
  - **`match_statistics.py`** : Classe pour gérer les statistiques des matchs.
  - **`data_manager.py`** : Classe pour gérer le chargement et la sauvegarde des données.
- **`data/`** : Contient les fichiers de données JSON pour les joueurs, le staff, les équipes, les matchs, les entraînements, etc.
- **`archives/`** : Contient les archives des saisons précédentes.
- **`tools.py`** : Contient des fonctions utilitaires pour l'application.




