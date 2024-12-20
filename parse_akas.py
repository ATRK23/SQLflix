#Original Author : Nabil MUSTAFA
#Modified by: Arthur BAILLET

# Ouvrir le fichier en mode lecture seule
with open('../title.akas.tsv', 'r') as f:
    # Ignorer la première ligne qui contient les noms des attributs
    next(f)

    # Boucle sur chaque ligne du fichier
    for line in f:
        # Découper la ligne en attributs avec un séparateur de tabulation (\t)
        items = line.rstrip("\n").split("\t")

        # Vérifier si la ligne contient des données manquantes
        if items[0] == r'\N':
            continue  # Ignorer les lignes où le premier champ est \N

        # Initialisation de la chaîne de valeurs SQL
        sql_values = []

        # Indices des colonnes qui doivent être traitées comme des tableaux
        array_columns = [5, 6]  # index colonne tableau

        # Traiter chaque champ de la ligne
        for idx, item in enumerate(items):
            if item == r'\N':  # Gérer les valeurs nulles pour PostgreSQL
                sql_values.append("NULL")
            elif idx in array_columns:
                # Si c'est une colonne tableau, reformater avec des accolades
                array_values = item.split(",")  # Découper les éléments séparés par des virgules
                formatted_array = "{" + ",".join(f'"{v.strip()}"' for v in array_values) + "}"
                sql_values.append(f"'{formatted_array}'")
            else:
                # Échapper les apostrophes et ajouter des guillemets pour les autres colonnes
                sql_values.append(f"'{item.replace('\'', '\'\'')}'")

        # Créer la chaîne finale SQL
        string_final = f"INSERT INTO akas VALUES ( {', '.join(sql_values)} );"

        # Afficher la chaîne d'insertion SQL (ou envoyer à la base de données)
        print(string_final)
