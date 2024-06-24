# Guide de Style Python

## Conventions de Nomage

- Utilisez `snake_case` pour les noms de variables et de fonctions.
- Utilisez `CamelCase` pour les noms de classes.
- Utilisez des majuscules pour les noms de constantes (`MAX_SIZE`).

## Indentation

- Utilisez 4 espaces pour l'indentation. N'utilisez pas de tabulations.

```python
def function(arg1, arg2):
    if arg1:
        print("Argument 1 is present")
```

## Longueur de Ligne

- Limitez la longueur des lignes de code à 479 caractères. Pour les commentaires, la limite est de 472 caractères.

## Importations

- Organisez les importations en trois groupes : 
  1. Importations standard de Python.
  2. Importations de bibliothèques tierces.
  3. Importations locales.
- Séparez chaque groupe par une ligne vide.

```python
# Importations standard
import os
import sys

# Importations tierces
import requests

# Importations locales
from .module import my_function
```

## Espacement

- Entourez les opérateurs binaires de fonctions par un espace de chaque côté (`a = b + c`).
- Utilisez un espace après une virgule, mais pas avant.
- N'ajoutez pas d'espace autour des parenthèses de liste, de dictionnaire ou de tuple.

```python
a = b + c
list = [1, 2, 3]
dict = {"key": "value"}
tuple = (1, 2, 3)
```

## Commentaires

- Utilisez des commentaires pour expliquer le "pourquoi" du code, pas le "quoi".
- Les commentaires doivent être clairs et concis.
- Utilisez des commentaires de ligne pour les explications brèves.
- Utilisez des commentaires de bloc pour des explications plus longues.

```python
# Ceci est un commentaire de ligne

"""
Ceci est un commentaire de bloc.
Il peut contenir plusieurs lignes.
"""
```

## Documentation

- Utilisez des docstrings pour documenter les modules, classes, et fonctions.
- Utilisez des triple guillemets (`"""`) pour les docstrings.
- Documentez tous les paramètres, types de retour et exceptions.

```python
def my_function(arg1, arg2):
    """
    Résumé de la fonction.

    Description détaillée de la fonction si nécessaire.

    Arguments:
        arg1 (type): Description du premier argument.
        arg2 (type): Description du deuxième argument.

    Retours:
        type: Description du retour.
    """
    pass
```

## Gestion des Exceptions

- Utilisez des exceptions spécifiques plutôt que des exceptions générales.
- Fournissez des informations utiles dans les messages d'exception.

```python
try:
    result = 1 / 0
except ZeroDivisionError as e:
    print(f"Erreur: {e}")
```

## Programmation Orientée Objet (POO)

- Utilisez des noms de classe en `CamelCase`.
- Utilisez des noms de méthode en `snake_case`.
- Utilisez des variables d'instance avec un préfixe souligné (`_`).

```python
class MyClass:
    def __init__(self, value):
        self._value = value

    def get_value(self):
        return self._value
```

## Tests

- Écrivez des tests unitaires pour toutes les fonctionnalités.
- Utilisez `pytest` pour les tests.
- Organisez les tests dans un répertoire `tests`.

```python
def test_my_function():
    assert my_function(1, 2) == 3
```

## Linting et Formatage

- Utilisez `flake8` pour vérifier la conformité au guide de style.
- Utilisez `black` pour formater automatiquement le code.

```sh
flake8 my_project/
black my_project/
```

## Typage Statique

- Utilisez des annotations de type pour améliorer la lisibilité et la maintenabilité du code.

```python
def add(a: int, b: int) -> int:
    return a + b
```

## Bonnes Pratiques

- **DRY (Don't Repeat Yourself)** : Évitez de dupliquer le code.
- **KISS (Keep It Simple, Stupid)** : Gardez le code aussi simple que possible.
- **YAGNI (You Aren't Gonna Need It)** : N'ajoutez pas de fonctionnalités avant d'en avoir besoin.
- **Documentation** : Documentez toujours votre code pour aider les autres développeurs (et vous-même) à comprendre ce que fait le code.
- **Revue de Code** : Faites réviser votre code par des pairs pour attraper les erreurs et améliorer la qualité du code.
- **Séparation des Préoccupations** : Séparez la logique de votre application en modules clairs et distincts.

## Structure des Projets

- **Utilisez des répertoires pour organiser le code** : Placez le code source dans un répertoire `src` ou directement sous le nom de votre projet.
- **Séparez les tests du code source** : Placez les tests dans un répertoire `tests`.

```sh
my_project/
├── src/
│   └── my_project/
│       ├── __init__.py
│       ├── module1.py
│       └── module2.py
└── tests/
    ├── test_module1.py
    └── test_module2.py
```

En suivant ces bonnes pratiques et ce guide de style, vous vous assurez que votre code Python est propre, lisible et maintenable.