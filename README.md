# GUDLFT

Plateforme de réservation de compétitions pour clubs de force, écrite en Flask.

## 1. Présentation

GUDLFT Registration est une application permettant à un secrétaire de club de :
- se connecter avec son adresse email ;
- visualiser la liste des compétitions à venir ;
- réserver des places en utilisant les points disponibles de son club ;
- consulter publiquement le tableau des points de tous les clubs.


## 2. Technologies

- **[Python](https://www.python.org) 3.11.15**
- **[Flask](https://flask.palletsprojects.com/)** - framework web léger
- **[pytest](https://docs.pytest.org/)** - framework de tests
- **[pytest-cov](https://pytest-cov.readthedocs.io/) / [coverage](https://coverage.readthedocs.io/)** - mesure de couverture
- **[pytest-integration](https://pypi.org/project/pytest-integration/)** - classification des tests par criticité
- **[Selenium](https://www.selenium.dev/)** - tests fonctionnels navigateur
- **[Locust](https://locust.io/)** - tests de performance

## 3. Installation

```bash
git clone https://github.com/myriamdesporte/GUDLFT.git
cd GUDLFT

# Environnement virtuel
python -m venv .venv
source .venv/bin/activate          # macOS / Linux
.venv\Scripts\activate           # Windows

# Dépendances
pip install -r requirements.txt
```

## 4. Lancer l'application

```bash
flask run
```

L'application est alors accessible sur `http://127.0.0.1:5000/`.

## 5. Lancer les tests

Trois niveaux de tests cohabitent dans le projet :

### 5.1 Tests unitaires et d'intégration (pytest)

```bash
# Tous les tests unitaires + intégration
pytest
pytest --with-integration --with-slow-integration

# Avec couverture et rapport HTML détaillé
pytest --cov=server --cov=helpers --cov-report=html tests/unit/ tests/helpers/
# puis ouvrir htmlcov/index.html
```

**Couverture actuelle : 98 % global (`server.py` 97 %, `helpers.py` 100 %). 58 tests passent + 2 fonctionnels skippés par défaut.**

### 5.2 Tests fonctionnels (Selenium)

Les tests dans `tests/functional/` ouvrent un vrai navigateur et nécessitent un serveur Flask actif et ChromeDriver installé.

```bash
# Terminal 1 : lancer l'application
flask run

# Terminal 2 : lancer les tests fonctionnels
pytest -m functional
```

Par défaut `pytest.ini` contient `addopts = -m "not functional"`, donc les tests fonctionnels 
sont automatiquement skippés lors d'un `pytest` ordinaire. Pour les lancer, on passe explicitement `-m functional` qui prend le pas sur le filtre par défaut.

### 5.3 Tests de performance (Locust)

```bash
# Terminal 1 : lancer l'application
flask run

# Terminal 2 : lancer Locust
locust -f tests/performance/locustfile.py --host=http://127.0.0.1:5000

# Ouvrir http://localhost:8089 et choisir le nombre d'utilisateurs + spawn rate
```

Trois scénarios : consultation du tableau public, login, et flux complet de réservation.

## 6. Structure des branches

Ce projet suit un git flow séquentiel : chaque correction de bug ou ajout de fonctionnalité a sa propre branche, créée depuis `QA` après que les fixes précédents y ont été mergés.

| Branche                               | Rôle                                                                                        |
|---------------------------------------|---------------------------------------------------------------------------------------------|
| `master`                              | État d'origine du POC OpenClassrooms, intact                                                |
| `QA`                                  | Branche d'intégration où chaque bug / feature est mergé. **Branche par défaut sur GitHub.** |
| `bug/unknown-email-crashes-app`       | Bug #1 — Crash lors d'un login avec email inconnu                                           |
| `bug/points-not-deducted`             | Bug #6 — Les points ne sont pas déduits après réservation                                   |
| `bug/book-past-competitions`          | Bug #5 — Réservation possible sur des compétitions passées                                  |
| `bug/use-more-points-than-allowed`    | Bug #2 — Un club peut réserver plus de places qu'il n'a de points                           |
| `bug/book-more-than-12-places`        | Bug #4 — Un club peut réserver plus de 12 places à une compétition                          |
| `bug/book-more-than-available-places` | Bug #282 — Réservation possible au-delà des places restantes                                |
| `feature/points-display-board`        | Feature #7 — Tableau public des points par club                                             |
|`test/add-integration-functional-performance-tests`| Branche de tests intégration, fonctionnels et performance                                   |

## 7. Architecture du code

`server.py` expose les routes Flask et importe trois helpers de recherche depuis `helpers.py` :

- `find_club_by_email(clubs, email)` - recherche d'un club par email (case-insensitive, tolère les espaces)
- `find_club(clubs, name)` - recherche d'un club par son nom
- `find_competition(competitions, name)` - recherche d'une compétition par son nom

Toutes ces helpers sont des fonctions **pures** : elles reçoivent la collection en argument et renvoient `None` si rien ne correspond. Elles sont testées indépendamment dans `tests/unit/test_helpers.py` (couverture 100 %).

Un context processor `inject_now` rend la date courante disponible dans tous les templates, ce qui permet à `welcome.html` de masquer le lien de réservation des compétitions passées.

## 8. Tests unitaires

Les tests unitaires vivent dans `tests/unit/` et utilisent :

- la fixture **`monkeypatch`** native de pytest, via une fixture **`autouse=True`** par classe de test, pour remplacer `server.clubs` et `server.competitions` par les fausses données ;
- les fixtures partagées **`mock_clubs`** et **`mock_competitions`** définies dans `tests/conftest.py`.

Conséquence : chaque test est isolé du fichier `competitions.json` réel, et la suite reste déterministe quelles que soient les modifications des données de production.

## 9. Données

`competitions.json` contient deux compétitions :
- **Spring Festival** (2026-03-27) - Date passée par rapport à aujourd'hui
- **Fall Classic** (2026-10-22) - Date à venir

Cette configuration permet à l'application d'illustrer immédiatement le filtrage des compétitions passées.

`clubs.json` contient trois clubs : `Simply Lift`, `Iron Temple`, `She Lifts`, avec des emails respectifs `john@simplylift.co`, `admin@irontemple.com`, `kate@shelifts.co.uk`.