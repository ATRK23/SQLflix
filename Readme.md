# SQLflix
Un moteur de recherche dans une base de données de films

## Auteurs

- Arthur BAILLET - 12107785
- Samy HALIT - 12200614
- Samy Amine HALIT - 12200840


## Fonctionnalités

- Recherche de films
- Triage des films par genre, mots clés, date, rang/note de utilisateurs
- Affichage des affiches/posters des films
- Possibilité de créer un compte utilisateurs
- Possibilité de se souvenir du dernier utilisateur connecté et de garder sa session active
- Possibilité de liker ou disliker un films
- Possibilité de noter un film et de laisser un avis / commentaire (visible par tous les utilisateurs)
- Possibilité de se créer des playlists (watchlists)
- Affichage d'autre informations sur les films
- Connection par mot de passe sécurisée


## Installation
Pour parser les bases données, vous aurez besoins des fichiers 
- ```tmdb_5000_movies.csv```
- ```tmdb_5000_credits.csv```
- ```SQLFLIX-createschema.sql```
- ```myparseCSV.py```
Et d'une base de données déjà paramétrée sur ```PostGreSQL```

Prérequis : Installer le module python ```pandas```
```bash
sudo apt update && sudo apt install python3-pandas
```
Ou, sous un environnement virtuel 
```
pip install pandas
```

Une fois installé, vous pouvez commencer à parser les bases de données, en vous assurant que les trois fichiers requis sont dans votre répertoire courant, avec la commande : 
```bash
python3 myparseCSV.py
```

Cela va créer un nouveau fichier  ```SQLFLIX-data.sql```. Ce fichier contient les informations des deux bases de données compilées dans un fichier compréhensible par le logiciel ```PostGreSQL```

Ensuite, connectez-vous à votre base de donnée PostGreSQL et entrer les deux commande suivante
```sql
\i SQLFLIX-createschema.sql
```
Et
```sql
\i SQLFLIX-data.sql
```
(La deuxième peut prendre un peu de temps).

Une fois terminée, l'installation et terminée et le programme peut être executé correctement.
## Utilisation
Une fois l'installation terminée, executer le programme avec
```bash
python3 SQLFLIX.py
```
Une fenètre s'ouvrira et vous pourrez vous créer un compte utilisateur et utiliser le logiciel