import sys
import psycopg2
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QLabel, QPushButton, QWidget, QTableWidget, QTableWidgetItem, QLineEdit, QGroupBox, QHBoxLayout
from PyQt5.QtCore import Qt

# Configuration PostgreSQL
DB_CONFIG = {
    'dbname': 'sqlflix',
    'user': 'postgres',
    'password': 'database12@',
    'host': 'localhost',
    'port': '5432'
}


class HomePage(QMainWindow):
    def __init__(self, username):
        super().__init__()

        self.username = username
        self.setWindowTitle("SQLFLIX - Homepage")
        self.setGeometry(100, 100, 800, 600)

        #Layout principal
        main_layout = QVBoxLayout()

        #Barre de recherche
        self.create_search_bar(main_layout)

        #Sections pour les films
        self.create_all_movies_section(main_layout)
        self.create_top_movies_section(main_layout)
        self.create_recommendations_section(main_layout)

        #Bouton de déconnexion
        self.logout_button = QPushButton("Logout")
        self.logout_button.clicked.connect(self.logout)
        main_layout.addWidget(self.logout_button)

        #Widget principal
        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)


    def create_search_bar(self, layout):
        """Crée une barre de recherche pour les films"""
        search_layout = QHBoxLayout()

        #Champ de recherche
        self.search_input = QLineEdit(self)
        self.search_input.setPlaceholderText("Search for a movie...")
        self.search_input.textChanged.connect(self.filter_movies)

        search_layout.addWidget(self.search_input)
        layout.addLayout(search_layout)

    def filter_movies(self):
        """Filtre les films affichés en fonction de la recherche dans 'Tous les films'"""
        search_text = self.search_input.text().lower()

        # Filtrer uniquement les films dans la section "Tous les films"
        filtered_movies = self.get_filtered_movies(search_text)

        # Mettre à jour la table des films avec les résultats
        self.update_movie_table(filtered_movies)

    def create_all_movies_section(self, layout):
        """Créer la section de tous les films"""
        all_movies_group = QGroupBox("Tous les Films")
        all_movies_layout = QVBoxLayout()

        # Créer une table pour afficher tous les films
        self.all_movies_table = QTableWidget()
        self.all_movies_table.setColumnCount(4)  # 4 colonnes: Title, Genre, Year, Rating
        self.all_movies_table.setHorizontalHeaderLabels(['Title', 'Genre', 'Year', 'Rating'])

        # Charger tous les films
        self.load_all_movies(self.all_movies_table)

        all_movies_layout.addWidget(self.all_movies_table)
        all_movies_group.setLayout(all_movies_layout)
        layout.addWidget(all_movies_group)
    
    def create_top_movies_section(self, layout):
        """Créer la section des films populaires"""
        top_movies_group = QGroupBox("Top 10 Films")
        top_movies_layout = QVBoxLayout()

        # Crée une table pour les films
        top_movies_table = QTableWidget()
        top_movies_table.setColumnCount(4)
        top_movies_table.setHorizontalHeaderLabels(['Title', 'Genre', 'Year', 'Rating'])

        # Charger les films à partir de la base de données
        self.load_top_movies(top_movies_table)

        top_movies_layout.addWidget(top_movies_table)
        top_movies_group.setLayout(top_movies_layout)
        layout.addWidget(top_movies_group)

    def create_recommendations_section(self, layout):
        recommendations_group = QGroupBox("Recommandations")
        recommendations_layout = QVBoxLayout()

        # Créer une table pour les recommandations
        recommendations_table = QTableWidget()
        recommendations_table.setColumnCount(4)
        recommendations_table.setHorizontalHeaderLabels(['Title', 'Genre', 'Release Date', 'Rating'])

        # Charger les recommandations
        self.load_recommendations(recommendations_table)

        recommendations_layout.addWidget(recommendations_table)
        recommendations_group.setLayout(recommendations_layout)
        layout.addWidget(recommendations_group)

    def load_all_movies(self, table):
        try:
            conn = psycopg2.connect(**DB_CONFIG)
            cursor = conn.cursor()
            query = """SELECT M.title, G.name as genre, M.release_date, M.vote_average
                    FROM movies AS M
                    INNER JOIN movie_genres AS MG ON M.movie_id = MG.movie_id
                    INNER JOIN genres AS G ON MG.genre_id = G.genre_id;"""
            cursor.execute(query)
            movies = cursor.fetchall()

            table.setRowCount(len(movies))
            for row, movie in enumerate(movies):
                table.setItem(row, 0, QTableWidgetItem(movie[0]))
                table.setItem(row, 1, QTableWidgetItem(movie[1]))
                table.setItem(row, 2, QTableWidgetItem(str(movie[2])))
                table.setItem(row, 3, QTableWidgetItem(str(movie[3])))

            cursor.close()
            conn.close()
        except Exception as e:
            print(f"Error loading all movies: {e}")

    def load_top_movies(self, table):
        try:
            conn = psycopg2.connect(**DB_CONFIG)
            cursor = conn.cursor()
            query = """SELECT M.title, G.name as genre, M.release_date, M.vote_average
                        FROM movies AS M
                        INNER JOIN movie_genres AS MG ON M.movie_id = MG.movie_id
                        INNER JOIN genres AS G ON MG.genre_id = G.genre_id
                        ORDER BY M.vote_average DESC
                        LIMIT 10;"""
            cursor.execute(query)
            movies = cursor.fetchall()

            table.setRowCount(len(movies))
            for row, movie in enumerate(movies):
                table.setItem(row, 0, QTableWidgetItem(movie[0]))
                table.setItem(row, 1, QTableWidgetItem(movie[1]))
                table.setItem(row, 2, QTableWidgetItem(str(movie[2])))
                table.setItem(row, 3, QTableWidgetItem(str(movie[3])))

            cursor.close()
            conn.close()
        except Exception as e:
            print(f"Error loading top movies: {e}")

    def load_recommendations(self, table):
        try:
            conn = psycopg2.connect(**DB_CONFIG)
            cursor = conn.cursor()
            query = """SELECT M.title, G.name as genre, M.release_date, M.vote_average
                        FROM movies AS M
                        INNER JOIN movie_genres AS MG ON M.movie_id = MG.movie_id
                        INNER JOIN genres AS G ON MG.genre_id = G.genre_id
                        ORDER BY M.vote_average DESC
                        LIMIT 5;"""
            cursor.execute(query)
            movies = cursor.fetchall()

            table.setRowCount(len(movies))
            for row, movie in enumerate(movies):
                table.setItem(row, 0, QTableWidgetItem(movie[0]))
                table.setItem(row, 1, QTableWidgetItem(movie[1]))
                table.setItem(row, 2, QTableWidgetItem(str(movie[2])))
                table.setItem(row, 3, QTableWidgetItem(str(movie[3])))

            cursor.close()
            conn.close()
        except Exception as e:
            print(f"Error loading recommendations: {e}")

    def get_filtered_movies(self, search_text):
        try:
            conn = psycopg2.connect(**DB_CONFIG)
            cursor = conn.cursor()

            query = """SELECT M.title, G.name as genre, M.release_date, M.vote_average
                    FROM movies AS M
                    INNER JOIN movie_genres AS MG ON M.movie_id = MG.movie_id
                    INNER JOIN genres AS G ON MG.genre_id = G.genre_id
                    WHERE M.title ILIKE %s;"""
            cursor.execute(query, ('%' + search_text + '%',))
            movies = cursor.fetchall()

            return [{"title": movie[0], "genre": movie[1], "release_date": movie[2], "vote_average": movie[3]} for movie in movies]

        except Exception as e:
            print(f"Error: {e}")
            return []
        finally:
            cursor.close()
            conn.close()

    def update_movie_table(self, movies):
        self.all_movies_table.setRowCount(len(movies))  # Mettre à jour la table des films

        for row, movie in enumerate(movies):
            self.all_movies_table.setItem(row, 0, QTableWidgetItem(movie["title"]))
            self.all_movies_table.setItem(row, 1, QTableWidgetItem(movie["genre"]))  # Affichage du genre
            self.all_movies_table.setItem(row, 2, QTableWidgetItem(str(movie["release_date"])))
            self.all_movies_table.setItem(row, 3, QTableWidgetItem(str(movie["vote_average"])))

    def logout(self):
        self.close()  # Fermer la fenêtre actuelle (page d'accueil)
        self.open_login_window()  # Ouvrir la page de connexion

    def open_login_window(self):
        from connexion_page import LoginWindow  # Importer la classe LoginWindow
        self.login_window = LoginWindow()  # Créer la fenêtre de connexion
        self.login_window.show()  # Afficher la fenêtre
