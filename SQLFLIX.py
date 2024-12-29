import sys
import psycopg2
import hashlib
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QLineEdit, QPushButton,
    QLabel, QMessageBox, QWidget, QDialog, QSpacerItem, QSizePolicy, QHBoxLayout, QCheckBox,
    QTableWidget, QTableWidgetItem, QGroupBox, QTabWidget, QSplitter, QScrollArea, QSlider, QFrame, QGridLayout, QHeaderView, QInputDialog, QComboBox
)
from PyQt5.QtGui import QPixmap, QFont, QIcon
from PyQt5.QtCore import Qt
import requests

# Configuration PostgreSQL 
DB_CONFIG = {
    'dbname': 'sqlflix',
    'user': 'postgres',
    'password': 'database12@',
    'host': 'localhost'
    #'port': '5432'
}

#API TMDB pour les poster
tmdb_api_key = "e072012ac707cd3cd0d66699ebce5aff"

BASE_URL = 'https://api.themoviedb.org/3'
IMAGE_BASE_URL = 'https://image.tmdb.org/t/p/w500'

def get_movie_poster_api(movie_name):
    search_url = f"{BASE_URL}/search/movie"
    params = {
        'api_key': tmdb_api_key,
        'query': movie_name
    }
    try:
        response = requests.get(search_url, params=params)
        response.raise_for_status()
        data = response.json()
        
        if data['results']:
            movie = data['results'][0]
            poster_path = movie['poster_path']
            poster_url = f"{IMAGE_BASE_URL}{poster_path}"
            return poster_url
        else:
            print("Film non trouvé.")
            return None
    except ConnectionError:
        print("Erreur de connexion : Impossible d'accéder à l'API TMDB.")
        return None

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("SQLFLIX - Sign in")
        #self.setGeometry(300, 300, 400, 500)
        screen = QApplication.primaryScreen()
        size = screen.availableGeometry()
        self.move(size.width() // 2 - self.width() // 2, size.height() // 2 - self.height() // 2)
        
        self.setWindowIcon(QIcon("icone.png"))

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        self.image_label = QLabel(self)
        self.pixmap = QPixmap("background.png")
        self.pixmap = self.pixmap.scaled(self.centralWidget().size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.image_label.setPixmap(self.pixmap)
        self.image_label.setScaledContents(True)
        self.layout.addWidget(self.image_label)

        title_label = QLabel("Connection to SQLFLIX", self)
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(title_label)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.username_input.setStyleSheet("padding: 10px; border-radius: 5px; border: 1px solid #ccc;")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet("padding: 10px; border-radius: 5px; border: 1px solid #ccc;")
        self.layout.addWidget(self.username_input)
        self.layout.addWidget(self.password_input)

        self.show_password_checkbox = QCheckBox("Show the password")
        self.show_password_checkbox.stateChanged.connect(self.toggle_password_visibility)
        self.layout.addWidget(self.show_password_checkbox)

        self.login_button = QPushButton("Sign in")
        self.signup_button = QPushButton("Sign up")
        self.login_button.setStyleSheet(
            "padding: 10px 20px; border-radius: 5px; background-color: #0078d7; color: white;"
        )
        self.signup_button.setStyleSheet(
            "padding: 10px 20px; border-radius: 5px; background-color: #5c5c5c; color: white;"
        )

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.login_button)
        button_layout.addWidget(self.signup_button)
        self.layout.addLayout(button_layout)

        self.password_input.returnPressed.connect(self.authenticate)
        self.login_button.clicked.connect(self.authenticate)
        self.signup_button.clicked.connect(self.open_signup_window)

        self.central_widget.setLayout(self.layout)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if not self.pixmap.isNull():
            scaled_pixmap = self.pixmap.scaled(
                self.image_label.width(), self.image_label.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            self.image_label.setPixmap(scaled_pixmap)

    def authenticate(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if self.check_credentials(username, password):
            QMessageBox.information(self, "Success", "Successful Connection !")
            self.close()
            self.open_home_page()
        else:
            QMessageBox.warning(self, "Error", "Invalid username or password.")
    
    def open_home_page(self):
        username = self.username_input.text()
        self.home_page = HomePage(username)
        self.home_page.show()
        self.close()
    
    def toggle_password_visibility(self):
        if self.show_password_checkbox.isChecked():
            self.password_input.setEchoMode(QLineEdit.Normal)
        else:
            self.password_input.setEchoMode(QLineEdit.Password)

    def check_credentials(self, username, password):
        try:
            conn = psycopg2.connect(**DB_CONFIG)
            cursor = conn.cursor()
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            query = "SELECT * FROM users WHERE username = %s AND password_hash = %s"
            cursor.execute(query, (username, hashed_password))
            user = cursor.fetchone()
            cursor.close()
            conn.close()
            return user is not None
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Problem with the database : {e}")
            return False

    def open_signup_window(self):
        signup_window = SignupWindow()
        signup_window.exec_()

class SignupWindow(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("SQLFLIX - Sign up")
        self.setGeometry(400, 300, 350, 400)

        self.layout = QVBoxLayout()

        title_label = QLabel("Create an account")
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(title_label)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.username_input.setStyleSheet("padding: 10px; border-radius: 5px; border: 1px solid #ccc;")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet("padding: 10px; border-radius: 5px; border: 1px solid #ccc;")
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setPlaceholderText("Confirm password")
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        self.confirm_password_input.setStyleSheet("padding: 10px; border-radius: 5px; border: 1px solid #ccc;")

        self.layout.addWidget(self.username_input)
        self.layout.addWidget(self.password_input)
        self.layout.addWidget(self.confirm_password_input)

        self.signup_button = QPushButton("Sign up")
        self.signup_button.setStyleSheet(
            "padding: 10px 20px; border-radius: 5px; background-color: #0078d7; color: white;"
        )
        self.signup_button.clicked.connect(self.register_user)

        self.layout.addWidget(self.signup_button, alignment=Qt.AlignCenter)

        self.setLayout(self.layout)

    def register_user(self):
        username = self.username_input.text().strip()
        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()

        if password != confirm_password:
            QMessageBox.warning(self, "Error", "The passwords do not match.")
            return

        if not username or not password:
            QMessageBox.warning(self, "Error", "Please fill in all the fields.")
            return

        try:
            conn = psycopg2.connect(**DB_CONFIG)
            cursor = conn.cursor()

            hashed_password = hashlib.sha256(password.encode()).hexdigest()

            query = "INSERT INTO users (username, password_hash) VALUES (%s, %s)"
            cursor.execute(query, (username, hashed_password))
            conn.commit()

            cursor.close()
            conn.close()

            QMessageBox.information(self, "Successful registration §", "You can now connect.")
            self.close()
        except psycopg2.IntegrityError:
            QMessageBox.critical(self, "Error", "This username is already taken.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Problem with the database : {e}")

class HomePage(QMainWindow):
    def __init__(self, username):
        super().__init__()

        self.username = username
        self.playlist_manager = PlaylistManager(DB_CONFIG)  
        self.setWindowTitle("SQLFLIX - Homepage")
        #self.setGeometry(100, 100, 800, 600)
        screen = QApplication.primaryScreen()
        size = screen.availableGeometry()
        self.resize(int(size.width() * 0.8), int(size.height() * 0.8))
        self.move(size.width() // 2 - self.width() // 2, size.height() // 2 - self.height() // 2)
        
        main_layout = QVBoxLayout()

        splitter = QSplitter(Qt.Horizontal)

        left_widget = QWidget()
        left_layout = QVBoxLayout()
        self.create_search_bar(left_layout)
        self.create_all_movies_section(left_layout)
        self.create_top_movies_section(left_layout)
        self.create_playlists_section(left_layout)
        #self.create_recommendations_section(left_layout)
        left_widget.setLayout(left_layout)
        
        right_widget = QWidget()
        right_layout = QVBoxLayout()
        self.tabs = QTabWidget()  # Les onglets pour afficher les films détaillés
        right_layout.addWidget(self.tabs)
        right_widget.setLayout(right_layout)
        
        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)

        main_layout.addWidget(splitter)

        # Logout button
        self.logout_button = QPushButton("Logout")
        self.logout_button.clicked.connect(self.logout)
        main_layout.addWidget(self.logout_button)

        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
        


    def create_search_bar(self, layout):
        search_layout = QHBoxLayout()

        # Menu déroulant pour les genres
        self.genre_filter = QComboBox(self)
        self.genre_filter.addItem("All Genres")  # Option par défaut
        self.load_genres()  # Charger les genres disponibles
        self.genre_filter.currentIndexChanged.connect(self.filter_movies)
        search_layout.addWidget(self.genre_filter)

        # Champ pour rechercher par titre
        self.search_input = QLineEdit(self)
        self.search_input.setPlaceholderText("Search by title...")
        self.search_input.textChanged.connect(self.filter_movies)
        search_layout.addWidget(self.search_input)

        # Champ pour rechercher par mot-clé
        self.keyword_input = QLineEdit(self)
        self.keyword_input.setPlaceholderText("Search by keyword...")
        self.keyword_input.textChanged.connect(self.filter_movies)
        search_layout.addWidget(self.keyword_input)

        layout.addLayout(search_layout)


    def load_genres(self):
        """Charge les genres disponibles à partir de la base de données et les ajoute au menu déroulant."""
        try:
            conn = psycopg2.connect(**DB_CONFIG)
            cursor = conn.cursor()
            query = "SELECT name FROM genres;"
            cursor.execute(query)
            genres = cursor.fetchall()
            for genre in genres:
                self.genre_filter.addItem(genre[0])  # Ajouter chaque genre à la liste
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"Error loading genres: {e}")


    def filter_movies_by_genre(self):
        """Filtre les films en fonction du genre sélectionné."""
        selected_genre = self.genre_filter.currentText()
        if selected_genre == "All Genres":
            self.load_all_movies(self.all_movies_table)  # Charger tous les films
        else:
            self.load_movies_by_genre(selected_genre)

    def load_movies_by_genre(self, genre):
        """Charge les films correspondant au genre sélectionné."""
        try:
            conn = psycopg2.connect(**DB_CONFIG)
            cursor = conn.cursor()
            query = """
                SELECT M.title, G.name as genre, M.release_date, M.vote_average
                FROM movies AS M
                INNER JOIN movie_genres AS MG ON M.movie_id = MG.movie_id
                INNER JOIN genres AS G ON MG.genre_id = G.genre_id
                WHERE G.name = %s
                ORDER BY M.title;
            """
            cursor.execute(query, (genre,))
            movies = cursor.fetchall()

            self.all_movies_table.setRowCount(len(movies))
            for row, movie in enumerate(movies):
                self.all_movies_table.setItem(row, 0, QTableWidgetItem(movie[0]))
                self.all_movies_table.setItem(row, 1, QTableWidgetItem(movie[1]))
                self.all_movies_table.setItem(row, 2, QTableWidgetItem(str(movie[2])))
                self.all_movies_table.setItem(row, 3, QTableWidgetItem(str(movie[3])))

            cursor.close()
            conn.close()
        except Exception as e:
            print(f"Error loading movies by genre: {e}")


    def filter_movies(self):
        """Filtre les films en fonction du titre, des mots-clés, et du genre."""
        selected_genre = self.genre_filter.currentText()
        search_text = self.search_input.text().strip().lower()
        keyword = self.keyword_input.text().strip().lower()

        filtered_movies = self.get_filtered_movies(selected_genre, search_text, keyword)
        self.update_movie_table(filtered_movies)


    def create_all_movies_section(self, layout):
        all_movies_group = QGroupBox("All movies")
        all_movies_layout = QVBoxLayout()

        self.all_movies_table = QTableWidget()
        self.all_movies_table.setColumnCount(4)
        self.all_movies_table.setHorizontalHeaderLabels(['Title', 'Genre', 'Year', 'Rating'])
        self.load_all_movies(self.all_movies_table)
        
        self.all_movies_table.resizeColumnsToContents()
        header = self.all_movies_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        
        self.all_movies_table.cellDoubleClicked.connect(self.on_movie_double_clicked)

        all_movies_layout.addWidget(self.all_movies_table)
        all_movies_group.setLayout(all_movies_layout)
        layout.addWidget(all_movies_group, stretch=1)
    
    def create_top_movies_section(self, layout):
        top_movies_group = QGroupBox("Top 10 Films")
        top_movies_layout = QVBoxLayout()

        self.top_movies_table = QTableWidget()
        self.top_movies_table.setColumnCount(4)
        self.top_movies_table.setHorizontalHeaderLabels(['Title', 'Genre', 'Year', 'Rating'])
        self.load_top_movies(self.top_movies_table)
        
        self.top_movies_table.resizeColumnsToContents()
        header = self.top_movies_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        
        self.top_movies_table.setFixedHeight(10 * self.top_movies_table.verticalHeader().defaultSectionSize())
        
        self.top_movies_table.cellDoubleClicked.connect(self.on_movie_double_clicked)

        top_movies_layout.addWidget(self.top_movies_table)
        top_movies_group.setLayout(top_movies_layout)
        layout.addWidget(top_movies_group, stretch=0)

    """ def create_recommendations_section(self, layout):
        self.recommendations_group = QGroupBox("Recommandations")
        self.recommendations_layout = QVBoxLayout()

        self.recommendations_table = QTableWidget()
        self.recommendations_table.setColumnCount(4)
        self.recommendations_table.setHorizontalHeaderLabels(['Title', 'Genre', 'Release Date', 'Rating'])
        self.load_recommendations(self.recommendations_table)
        
        self.recommendations_table.cellDoubleClicked.connect(self.on_movie_double_clicked)

        self.recommendations_layout.addWidget(self.recommendations_table)
        self.recommendations_group.setLayout(self.recommendations_layout)
        layout.addWidget(self.recommendations_group) """

    def load_all_movies(self, table):
        """Charge tous les films avec leurs genres combinés dans une seule colonne."""
        try:
            conn = psycopg2.connect(**DB_CONFIG)
            cursor = conn.cursor()
            query = """
                SELECT 
                    M.title,
                    STRING_AGG(DISTINCT G.name, ', ') AS genres, 
                    M.release_date, 
                    M.vote_average
                FROM 
                    movies AS M
                INNER JOIN 
                    movie_genres AS MG ON M.movie_id = MG.movie_id
                INNER JOIN 
                    genres AS G ON MG.genre_id = G.genre_id
                GROUP BY 
                    M.movie_id, M.title, M.release_date, M.vote_average
                ORDER BY 
                    M.title;
            """
            cursor.execute(query)
            movies = cursor.fetchall()

            table.setRowCount(len(movies))
            for row, movie in enumerate(movies):
                table.setItem(row, 0, QTableWidgetItem(movie[0]))  # Titre
                table.setItem(row, 1, QTableWidgetItem(movie[1]))  # Genres
                table.setItem(row, 2, QTableWidgetItem(str(movie[2])))  # Date de sortie
                table.setItem(row, 3, QTableWidgetItem(str(movie[3])))  # Moyenne des votes

            cursor.close()
            conn.close()
        except Exception as e:
            print(f"Error loading all movies: {e}")


    def load_top_movies(self, table):
        try:
            conn = psycopg2.connect(**DB_CONFIG)
            cursor = conn.cursor()
            query = """ SELECT 
                                M.title, 
                                string_agg(G.name, ', ') AS genres,
                                M.release_date, 
                                M.vote_average
                        FROM 
                                movies AS M
                                INNER JOIN 
                                movie_genres AS MG ON M.movie_id = MG.movie_id
                                INNER JOIN 
                                genres AS G ON MG.genre_id = G.genre_id
                        WHERE vote_count > 1000
                        GROUP BY 
                            M.movie_id, M.title, M.release_date, M.vote_average
                        ORDER BY (M.vote_average * LOG(1 + M.vote_count)) DESC
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

    def get_filtered_movies(self, selected_genre, search_text, keyword):
        try:
            conn = psycopg2.connect(**DB_CONFIG)
            cursor = conn.cursor()

            query = """
                SELECT 
                    M.title,
                    STRING_AGG(DISTINCT G.name, ', ') AS genres, 
                    M.release_date, 
                    M.vote_average
                FROM 
                    movies AS M
                LEFT JOIN 
                    movie_genres AS MG ON M.movie_id = MG.movie_id
                LEFT JOIN 
                    genres AS G ON MG.genre_id = G.genre_id
                LEFT JOIN 
                    movie_keywords AS MK ON M.movie_id = MK.movie_id
                LEFT JOIN 
                    keywords AS K ON MK.keyword_id = K.keyword_id
                WHERE 
                    (%s = 'All Genres' OR G.name = %s) AND
                    (%s = '' OR M.title ILIKE %s) AND
                    (%s = '' OR K.name ILIKE %s)
                GROUP BY 
                    M.movie_id, M.title, M.release_date, M.vote_average
                ORDER BY 
                    M.title;
            """

            cursor.execute(query, (
                selected_genre, selected_genre,  # Filtrage par genre
                search_text, f"%{search_text}%",  # Filtrage par titre
                keyword, f"%{keyword}%"  # Filtrage par mot-clé
            ))
            movies = cursor.fetchall()
            cursor.close()
            conn.close()

            return [{"title": movie[0], "genre": movie[1], "release_date": movie[2], "vote_average": movie[3]} for movie in movies]
        except Exception as e:
            print(f"Error fetching filtered movies: {e}")
            return []



    def update_movie_table(self, movies):
        self.all_movies_table.setRowCount(len(movies))
        for row, movie in enumerate(movies):
            self.all_movies_table.setItem(row, 0, QTableWidgetItem(movie["title"]))
            self.all_movies_table.setItem(row, 1, QTableWidgetItem(movie["genre"]))
            self.all_movies_table.setItem(row, 2, QTableWidgetItem(str(movie["release_date"])))
            self.all_movies_table.setItem(row, 3, QTableWidgetItem(str(movie["vote_average"])))

    def logout(self):
        self.close()
        self.open_login_window()

    def open_login_window(self):
        self.login_window = LoginWindow()
        self.login_window.show()
        
    def open_movie_page(self, movie_id, user_id):
        movie_name = get_movie_name(movie_id)
        movie_year = get_movie_year(movie_id)

        # Vérifier si l'onglet existe déjà
        for index in range(self.tabs.count()):
            if self.tabs.tabText(index) == f"{movie_name} ({movie_year})":
                self.tabs.setCurrentIndex(index)  # Sélectionner l'onglet existant
                return

        # Créer un nouvel onglet pour le film
        movie_page = MoviePage(movie_id, user_id)
        self.tabs.addTab(movie_page, f"{movie_name} ({movie_year})")
        self.tabs.setCurrentIndex(self.tabs.count() - 1)  # Sélectionner le dernier onglet

    def on_movie_double_clicked(self, row):
        
        table = self.sender() #recupere ce qui l'a appelé
        
        # Récupérer le titre et l'année du film
        movie_title = table.item(row, 0).text()
        release_date = table.item(row, 2).text()  # L'année est la 3e colonne
        movie_year = release_date.split('-')[0]

        # Rechercher l'ID du film à partir du titre et de l'année
        movie_id = self.get_movie_id_by_title_and_year(movie_title, movie_year)

        # Ouvrir la page du film
        if movie_id:
            self.open_movie_page(movie_id, self.get_user_id(self.username))
            
    def get_user_id(self, username):
        try:
            conn = psycopg2.connect(**DB_CONFIG)
            cursor = conn.cursor()
            query = "SELECT user_id FROM users WHERE username = %s"
            cursor.execute(query, (username,))
            user_id = cursor.fetchone()[0]
            cursor.close()
            conn.close()
            return user_id
        except Exception as e:
            print(f"Error: {e}")
            return None

    def get_movie_id_by_title_and_year(self, title, year):
        try:
            conn = psycopg2.connect(**DB_CONFIG)
            cursor = conn.cursor()

            # Convertir l'année en entier (si nécessaire)
            year = int(year)

            # Requête pour récupérer l'ID du film à partir du titre et de l'année
            query = """SELECT movie_id FROM movies WHERE title = %s AND EXTRACT(YEAR FROM release_date) = %s;"""
            cursor.execute(query, (title, year))
            movie_id = cursor.fetchone()

            cursor.close()
            conn.close()

            if movie_id:
                return movie_id[0]  # Retourner l'ID du film
            else:
                print(f"Film {title} ({year}) non trouvé.")
                return None

        except Exception as e:
            print(f"Erreur lors de la récupération de l'ID du film: {e}")
            return None

    def create_playlists_section(self, layout):
        playlists_group = QGroupBox("My Playlists")
        playlists_layout = QVBoxLayout()

        # Table pour afficher les playlists
        self.playlists_table = QTableWidget()
        self.playlists_table.setColumnCount(2)
        self.playlists_table.setHorizontalHeaderLabels(['Playlist Name', 'Actions'])
        self.load_playlists()

        # Bouton pour créer une nouvelle playlist
        create_button = QPushButton("Create Playlist")
        create_button.clicked.connect(self.create_playlist_ui)  # Lier au backend pour créer une playlist

        # Ajout des widgets au layout
        playlists_layout.addWidget(self.playlists_table)
        playlists_layout.addWidget(create_button)
        playlists_group.setLayout(playlists_layout)
        layout.addWidget(playlists_group)

    def load_playlists(self):
        playlists = self.playlist_manager.get_user_playlists(self.get_user_id(self.username))  # Récupérer les playlists

        self.playlists_table.setRowCount(len(playlists))
        self.playlists_table.setColumnCount(3)  # Nombre de colonnes
        self.playlists_table.setHorizontalHeaderLabels(['Playlist Name', 'View', 'Delete'])

        for row, playlist in enumerate(playlists):
            # Nom de la playlist
            playlist_name = QTableWidgetItem(playlist[1])
            self.playlists_table.setItem(row, 0, playlist_name)

            # Bouton "View"
            view_button = QPushButton("View")
            view_button.clicked.connect(lambda _, pid=playlist[0]: self.view_playlist(pid))
            self.playlists_table.setCellWidget(row, 1, view_button)

            # Bouton "Delete"
            delete_button = QPushButton("Delete")
            delete_button.clicked.connect(lambda _, pid=playlist[0]: self.delete_playlist(pid))
            self.playlists_table.setCellWidget(row, 2, delete_button)

    def view_playlist(self, playlist_id, movies_table=None):
        playlist_movies = self.playlist_manager.get_playlist_movies(playlist_id)

        if not movies_table:
            # Créer une nouvelle fenêtre uniquement si aucune table n'existe
            self.dialog = QDialog(self)
            self.dialog.setWindowTitle("Playlist Movies")
            self.dialog.setGeometry(200, 200, 600, 400)

            layout = QVBoxLayout(self.dialog)
            movies_table = QTableWidget()
            movies_table.setColumnCount(4)  # Inclure une colonne pour les actions
            movies_table.setHorizontalHeaderLabels(['Title', 'Release Date', 'Rating', 'Actions'])

            layout.addWidget(movies_table)
            self.dialog.setLayout(layout)
            self.dialog.show()

        # Remplir la table
        movies_table.setRowCount(len(playlist_movies))
        for row, movie in enumerate(playlist_movies):
            movies_table.setItem(row, 0, QTableWidgetItem(movie[0]))  # Title
            movies_table.setItem(row, 1, QTableWidgetItem(str(movie[1])))  # Release Date
            movies_table.setItem(row, 2, QTableWidgetItem(str(movie[2])))  # Rating

            # Ajouter le bouton "Remove"
            remove_button = QPushButton("Remove")
            remove_button.clicked.connect(lambda _, mid=movie[3]: self.remove_movie_from_playlist(playlist_id, mid, movies_table))
            movies_table.setCellWidget(row, 3, remove_button)

        # Ajuster la taille des colonnes
        movies_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)


    def create_playlist_ui(self):
        # Boîte de dialogue pour demander le nom de la playlist
        playlist_name, ok = QInputDialog.getText(self, "Create Playlist", "Enter playlist name:")
        if ok and playlist_name.strip():  # Vérifier si un nom a été saisi
           # Appeler le backend pour créer la playlist
            playlist_id = self.playlist_manager.create_playlist(self.get_user_id(self.username), playlist_name.strip())
            if playlist_id:
                QMessageBox.information(self, "Success", f"Playlist '{playlist_name}' created successfully!")
                self.load_playlists()  # Recharger la liste des playlists
            else:
                QMessageBox.warning(self, "Error", "Failed to create playlist.")
        else:
            QMessageBox.warning(self, "Invalid Input", "Playlist name cannot be empty.")

    def add_movie_to_playlist_ui(self, movie_id):
        playlists = self.playlist_manager.get_user_playlists(self.get_user_id(self.username))
        playlist_names = [playlist[1] for playlist in playlists]

        playlist_name, ok = QInputDialog.getItem(self, "Add to Playlist", "Select playlist:", playlist_names, editable=False)
        if ok and playlist_name:
            playlist_id = next(p[0] for p in playlists if p[1] == playlist_name)
            self.playlist_manager.add_movie_to_playlist(playlist_id, movie_id)
            QMessageBox.information(self, "Success", "Movie added to playlist!")

    def remove_movie_from_playlist(self, playlist_id, movie_id, movies_table):
        try:
            # Supprimer le film de la playlist via PlaylistManager
            self.playlist_manager.remove_movie_from_playlist(playlist_id, movie_id)
            QMessageBox.information(self, "Success", "Movie removed from playlist successfully!")

            # Rafraîchir la vue de la playlist
            self.view_playlist(playlist_id, movies_table)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to remove movie: {e}")

    def delete_playlist(self, playlist_id):
        reply = QMessageBox.question(
            self, "Confirm Deletion",
            "Are you sure you want to delete this playlist? This action cannot be undone.",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            try:
                # Supprimer la playlist via PlaylistManager
                self.playlist_manager.delete_playlist(playlist_id)
                QMessageBox.information(self, "Success", "Playlist deleted successfully!")

                # Recharger la liste des playlists
                self.load_playlists()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to delete playlist: {e}")

#----------------------------------------------------------

def get_movie_date(movie_id):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        query = "SELECT release_date FROM movies WHERE movie_id = %s"
        cursor.execute(query, (movie_id,))
        movie_date = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return movie_date
    except Exception as e:
        print(f"Error: {e}")
        return "Error get movie date"
    
def get_movie_year(movie_id):
    date = get_movie_date(movie_id)
    return date.year

def get_movie_name(movie_id):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        query = "SELECT title FROM movies WHERE movie_id = %s"
        cursor.execute(query, (movie_id,))
        movie_name = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return movie_name
    except Exception as e:
        print(f"Error: {e}")
        return "Movie Page"

class MoviePage(QMainWindow):
    def __init__(self, movie_id, user_id):
        super().__init__()
        self.like_button = QPushButton("👍 Like")
        self.dislike_button = QPushButton("👎 Dislike")

        self.movie_id = movie_id
        self.user_id = user_id

        self.setWindowTitle(f"SQLFLIX - {get_movie_name(movie_id)} ({get_movie_year(movie_id)})")
        self.setGeometry(100, 100, 1000, 600)

        splitter = QSplitter(Qt.Vertical)

        # Layouts gauche et droite
        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()

        # Partie gauche : Titre centré et image
        title_label = QLabel(get_movie_name(movie_id))
        title_label.setAlignment(Qt.AlignCenter)  # Centrer le titre
        title_label.setStyleSheet("font-size: 30px; font-weight: bold;")
        left_layout.addWidget(title_label)

        movie_name = get_movie_name(movie_id)

        poster_label = QLabel()
        poster_pixmap = self.get_movie_poster(movie_name)
        if poster_pixmap:
            poster_label.setPixmap(poster_pixmap)
        else:
            print("Erreur : Impossible de charger l'affiche du film.")
        poster_label.setPixmap(poster_pixmap)
        poster_label.setAlignment(Qt.AlignCenter)
        left_layout.addWidget(poster_label)
        
        # Bouton pour ajouter le film à une playlist
        add_to_playlist_button = QPushButton("Add to Playlist")
        add_to_playlist_button.clicked.connect(self.add_to_playlist_ui)
        left_layout.addWidget(add_to_playlist_button)  
        
        # Partie droite : Sections
        right_layout.addWidget(self.create_ratings_section())
        right_layout.addWidget(self.create_like_dislike_section(user_id, movie_id))
        right_layout.addWidget(self.create_genres_and_keywords_section(movie_id))
        right_layout.addWidget(self.create_languages_section(movie_id))

        # Disposition Cast et Crew côte à côte avec scrollbar
        cast_crew_layout = QHBoxLayout()
        cast_scroll = QScrollArea()
        cast_scroll.setWidget(self.create_cast_section(movie_id))
        cast_scroll.setWidgetResizable(True)
        cast_scroll.setFixedHeight(200)

        crew_scroll = QScrollArea()
        crew_scroll.setWidget(self.create_crew_section(movie_id))
        crew_scroll.setWidgetResizable(True)
        crew_scroll.setFixedHeight(200)

        cast_crew_layout.addWidget(cast_scroll)
        cast_crew_layout.addWidget(crew_scroll)
        cast_crew_widget = QWidget()
        cast_crew_widget.setLayout(cast_crew_layout)
        right_layout.addWidget(cast_crew_widget)

        right_widget = QWidget()
        right_widget.setLayout(right_layout)
        right_scroll_area = QScrollArea()
        right_scroll_area.setWidget(right_widget)
        right_scroll_area.setWidgetResizable(True)

        left_widget = QWidget()
        left_widget.setLayout(left_layout)
        splitter.addWidget(left_widget)
        splitter.addWidget(right_scroll_area)

        central_widget = QWidget()
        central_layout = QVBoxLayout()
        central_layout.addWidget(splitter)
        central_widget.setLayout(central_layout)

        self.setCentralWidget(central_widget)

    def get_movie_poster(self, movie_name):
        poster_url = get_movie_poster_api(movie_name)
        if poster_url:
            try:
                response = requests.get(poster_url, stream=True)
                if response.status_code == 200:
                    image_data = response.content
                    pixmap = QPixmap()
                    pixmap.loadFromData(image_data)
                    return pixmap
            except Exception as e:
                print(f"Erreur lors du téléchargement de l'image : {e}")
        return None

    def get_like_dislike_status(self, user_id, movie_id):
        try:
            conn = psycopg2.connect(**DB_CONFIG)
            cursor = conn.cursor()
            query = """SELECT liked FROM user_movie_interactions
                    WHERE user_id = %s AND movie_id = %s"""
            cursor.execute(query, (user_id, movie_id))
            result = cursor.fetchone()
            cursor.close()
            conn.close()

            if result is not None:
                return result[0]  # TRUE, FALSE, ou NULL
            return None  # Aucun enregistrement
        except Exception as e:
            print(f"Erreur lors de la récupération du statut like/dislike : {e}")
            return None

    def create_like_dislike_section(self, user_id, movie_id):
        like_dislike_group = QGroupBox("Like / Dislike")
        like_dislike_layout = QHBoxLayout()  # Mettre les boutons côte à côte

        # Utilisez les attributs de la classe
        like_button = self.like_button
        dislike_button = self.dislike_button

        # Récupérer l'état initial
        current_status = self.get_like_dislike_status(user_id, movie_id)

        # Appliquer un style visuel selon l'état
        if current_status is True:
            like_button.setStyleSheet("background-color: green; color: white;")
        elif current_status is False:
            dislike_button.setStyleSheet("background-color: red; color: white;")
        else:
            like_button.setStyleSheet("")
            dislike_button.setStyleSheet("")

        # Gérer les clics sur les boutons
        like_button.clicked.connect(lambda: self.handle_like_dislike(user_id, movie_id, True))
        dislike_button.clicked.connect(lambda: self.handle_like_dislike(user_id, movie_id, False))

        like_dislike_layout.addWidget(like_button)
        like_dislike_layout.addWidget(dislike_button)
        like_dislike_group.setLayout(like_dislike_layout)
        return like_dislike_group

    def handle_like_dislike(self, user_id, movie_id, liked):
        try:
            conn = psycopg2.connect(**DB_CONFIG)
            cursor = conn.cursor()

            # Vérifiez si une interaction existe déjà
            query_check = """SELECT liked FROM user_movie_interactions
                            WHERE user_id = %s AND movie_id = %s"""
            cursor.execute(query_check, (user_id, movie_id))
            result = cursor.fetchone()

            if result is None:
                # Insérer une nouvelle interaction
                query_insert = """INSERT INTO user_movie_interactions (user_id, movie_id, liked)
                                VALUES (%s, %s, %s)"""
                cursor.execute(query_insert, (user_id, movie_id, liked))
            else:
                # Mettre à jour l'interaction existante
                query_update = """UPDATE user_movie_interactions
                                SET liked = %s
                                WHERE user_id = %s AND movie_id = %s"""
                cursor.execute(query_update, (liked, user_id, movie_id))

            conn.commit()
            cursor.close()
            conn.close()

            # Mettre à jour l'interface (réinitialise les boutons)
            self.refresh_like_dislike_buttons(user_id, movie_id)
        except Exception as e:
            print(f"Erreur lors de la mise à jour like/dislike : {e}")

    def refresh_like_dislike_buttons(self, user_id, movie_id):
        """
        Rafraîchit les boutons Like/Dislike selon l'état actuel.
        """
        current_status = self.get_like_dislike_status(user_id, movie_id)

        # Met à jour le style des boutons
        if current_status is True:
            self.like_button.setStyleSheet("background-color: green; color: white;")
            self.dislike_button.setStyleSheet("")
        elif current_status is False:
            self.like_button.setStyleSheet("")
            self.dislike_button.setStyleSheet("background-color: red; color: white;")
        else:
            self.like_button.setStyleSheet("")
            self.dislike_button.setStyleSheet("")


    def create_ratings_section(self):
        ratings_group = QGroupBox("Ratings")
        ratings_layout = QVBoxLayout()  # Utilisez QVBoxLayout pour empiler verticalement

        # Affichage de la note moyenne
        try:
            conn = psycopg2.connect(**DB_CONFIG)
            cursor = conn.cursor()
            query = "SELECT vote_average, vote_count FROM movies WHERE movie_id = %s"
            cursor.execute(query, (self.movie_id,))
            result = cursor.fetchone()
            rating = result[0]
            count = result[1]
            cursor.close()
            conn.close()

            rating_label = QLabel(f"Average Rating: {rating:.1f} ({count} votes)")
            ratings_layout.addWidget(rating_label)
        except Exception as e:
            print(f"Error fetching rating: {e}")

        # Séparateur visuel
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        ratings_layout.addWidget(separator)

        # Texte explicatif pour le slider
        explanation_label = QLabel("Use the slider to rate this movie:")
        ratings_layout.addWidget(explanation_label)

        # Sélection de la note (slider interactif)
        slider_layout = QVBoxLayout()  # Utilisez QVBoxLayout pour empiler le slider et les labels
        slider = QSlider(Qt.Horizontal)
        slider.setRange(0, 5)
        slider.setTickInterval(1)
        slider.setTickPosition(QSlider.TicksBelow)

        # Initialiser le slider avec la note de l'utilisateur
        try:
            conn = psycopg2.connect(**DB_CONFIG)
            cursor = conn.cursor()
            query = "SELECT rating FROM user_movie_interactions WHERE user_id = %s AND movie_id = %s"
            cursor.execute(query, (self.user_id, self.movie_id))
            user_rating = cursor.fetchone()
            if user_rating is not None:
                slider.setValue(user_rating[0])
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"Error fetching user rating: {e}")

        def update_rating(value):
            try:
                conn = psycopg2.connect(**DB_CONFIG)
                cursor = conn.cursor()
                query = """INSERT INTO user_movie_interactions (user_id, movie_id, rating) 
                        VALUES (%s, %s, %s)
                        ON CONFLICT (user_id, movie_id) DO UPDATE SET rating = %s"""
                cursor.execute(query, (self.user_id, self.movie_id, value, value))
                conn.commit()
                cursor.close()
                conn.close()
            except Exception as e:
                print(f"Error updating rating: {e}")

        slider.valueChanged.connect(update_rating)
        slider_layout.addWidget(slider)
            
        labels_layout = QHBoxLayout()  # Utiliser un layout horizontal pour aligner les labels
        for i in range(6):
            label = QLabel(str(i))
            label.setAlignment(Qt.AlignCenter)
            labels_layout.addWidget(label)
            if i < 5:  # Ajouter un stretch entre les labels sauf après le dernier
                labels_layout.addStretch(1)

        ratings_layout.addLayout(slider_layout)
        ratings_layout.addLayout(labels_layout)

        ratings_group.setLayout(ratings_layout)
        return ratings_group


    def create_genres_and_keywords_section(self, movie_id):
        group = QGroupBox("Genres and Keywords")
        layout = QVBoxLayout()

        # Récupération des genres
        try:
            conn = psycopg2.connect(**DB_CONFIG)
            cursor = conn.cursor()
            query = """SELECT G.name FROM genres AS G
                    INNER JOIN movie_genres AS MG ON G.genre_id = MG.genre_id
                    WHERE MG.movie_id = %s"""
            cursor.execute(query, (movie_id,))
            genres = cursor.fetchall()
            genres_list = ", ".join([genre[0] for genre in genres])
            cursor.close()
            conn.close()

            layout.addWidget(QLabel(f"Genres: {genres_list}"))
        except Exception as e:
            print(f"Error fetching genres: {e}")

        # Récupération des mots-clés
        try:
            conn = psycopg2.connect(**DB_CONFIG)
            cursor = conn.cursor()
            query = """SELECT K.name FROM keywords AS K
                    INNER JOIN movie_keywords AS MK ON K.keyword_id = MK.keyword_id
                    WHERE MK.movie_id = %s LIMIT 5"""
            cursor.execute(query, (movie_id,))
            keywords = cursor.fetchall()
            keywords_list = ", ".join([kw[0] for kw in keywords])
            cursor.close()
            conn.close()

            layout.addWidget(QLabel(f"Keywords: {keywords_list}"))
        except Exception as e:
            print(f"Error fetching keywords: {e}")

        group.setLayout(layout)
        return group

    def create_languages_section(self, movie_id):
        group = QGroupBox("Languages")
        layout = QVBoxLayout()

        try:
            conn = psycopg2.connect(**DB_CONFIG)
            cursor = conn.cursor()
            query = """SELECT L.name, L.language_code FROM spoken_languages AS L
                    INNER JOIN movie_spoken_languages AS MSL ON L.language_code = MSL.language_code
                    WHERE MSL.movie_id = %s"""
            cursor.execute(query, (movie_id,))
            languages = cursor.fetchall()
            cursor.close()
            conn.close()

            # Construire une chaîne de caractères avec toutes les langues
            languages_str = ", ".join([f"{self.get_flag_emoji(code)} {language}" for language, code in languages])
            layout.addWidget(QLabel(languages_str))
        except Exception as e:
            print(f"Error fetching languages: {e}")

        group.setLayout(layout)
        return group

    def get_flag_emoji(self, language_code):
        if len(language_code) == 2:
            return chr(ord(language_code[0].upper()) + 127397) + chr(ord(language_code[1].upper()) + 127397)
        return "🏳️"

    def get_movie_cast(self, movie_id):
        try:
            conn = psycopg2.connect(**DB_CONFIG)
            cursor = conn.cursor()
            query = """SELECT actor_name, character_name
                    FROM movie_cast
                    WHERE movie_id = %s
                    ORDER BY display_order"""
            cursor.execute(query, (movie_id,))
            cast = cursor.fetchall()
            cursor.close()
            conn.close()
            return cast  # Liste de tuples (actor_name, character_name)
        except Exception as e:
            print(f"Erreur lors de la récupération du cast : {e}")
            return []

    def create_cast_section(self, movie_id):
        cast_group = QGroupBox("Cast")
        cast_layout = QVBoxLayout()

        cast = self.get_movie_cast(movie_id)

        if not cast:
            label = QLabel("No cast information available.")
            cast_layout.addWidget(label)
        else:
            for actor_name, character_name in cast:
                label = QLabel(f"{actor_name} as {character_name}")
                cast_layout.addWidget(label)

        cast_group.setLayout(cast_layout)
        return cast_group

    def get_movie_crew(self, movie_id):
        try:
            conn = psycopg2.connect(**DB_CONFIG)
            cursor = conn.cursor()
            query = """SELECT member_name, job
                    FROM crew
                    WHERE movie_id = %s
                    ORDER BY department"""
            cursor.execute(query, (movie_id,))
            crew = cursor.fetchall()
            cursor.close()
            conn.close()
            return crew  # Liste de tuples (member_name, job)
        except Exception as e:
            print(f"Erreur lors de la récupération du crew : {e}")
            return []
        
    def create_crew_section(self, movie_id):

        crew_group = QGroupBox("Crew")
        crew_layout = QVBoxLayout()

        crew = self.get_movie_crew(movie_id)

        if not crew:
            label = QLabel("No crew information available.")
            crew_layout.addWidget(label)
        else:
            for member_name, job in crew:
                label = QLabel(f"{member_name} - {job}")
                crew_layout.addWidget(label)

        crew_group.setLayout(crew_layout)
        return crew_group
    
    def add_to_playlist_ui(self):
        # Obtenez les playlists de l'utilisateur via PlaylistManager
        playlist_manager = PlaylistManager(DB_CONFIG)
        playlists = playlist_manager.get_user_playlists(self.user_id)
        playlist_names = [playlist[1] for playlist in playlists]  # Liste des noms des playlists

        if not playlist_names:
            QMessageBox.warning(self, "No Playlists", "You don't have any playlists. Please create one first.")
            return

        # Boîte de dialogue pour choisir une playlist
        playlist_name, ok = QInputDialog.getItem(self, "Add to Playlist", "Select playlist:", playlist_names, editable=False)
        if ok and playlist_name:
            # Trouver l'ID de la playlist sélectionnée
            playlist_id = next(p[0] for p in playlists if p[1] == playlist_name)
            playlist_manager.add_movie_to_playlist(playlist_id, self.movie_id)
            QMessageBox.information(self, "Success", f"Movie added to playlist '{playlist_name}'!")
        else:
            QMessageBox.warning(self, "Action Cancelled", "No playlist selected.")


class PlaylistManager:
    def __init__(self, db_config):
        self.db_config = db_config
        
    def create_playlist(self, user_id, playlist_name):
        try:
            conn = psycopg2.connect(**self.db_config)
            cursor = conn.cursor()
            query = "INSERT INTO playlists (user_id, name) VALUES (%s, %s) RETURNING playlist_id;"
            cursor.execute(query, (user_id, playlist_name))
            playlist_id = cursor.fetchone()[0]
            conn.commit()
            cursor.close()
            conn.close()
            return playlist_id
        except Exception as e:
            print(f"Error creating playlist: {e}")
            return None

    def add_movie_to_playlist(self, playlist_id, movie_id):
        try:
            conn = psycopg2.connect(**self.db_config)
            cursor = conn.cursor()
            query = "INSERT INTO playlist_movies (playlist_id, movie_id) VALUES (%s, %s);"
            cursor.execute(query, (playlist_id, movie_id))
            conn.commit()
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"Error adding movie to playlist: {e}")


    def remove_movie_from_playlist(self, playlist_id, movie_id):
        try:
            conn = psycopg2.connect(**self.db_config)
            cursor = conn.cursor()
            query = "DELETE FROM playlist_movies WHERE playlist_id = %s AND movie_id = %s;"
            cursor.execute(query, (playlist_id, movie_id))
            conn.commit()
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"Error removing movie from playlist: {e}")

    def get_user_playlists(self, user_id):
        try:
            conn = psycopg2.connect(**self.db_config)
            cursor = conn.cursor()
            query = "SELECT playlist_id, name FROM playlists WHERE user_id = %s;"
            cursor.execute(query, (user_id,))
            playlists = cursor.fetchall()
            cursor.close()
            conn.close()
            return playlists
        except Exception as e:
            print(f"Error fetching playlists: {e}")
            return []

    def get_playlist_movies(self, playlist_id):
        try:
            conn = psycopg2.connect(**self.db_config)
            cursor = conn.cursor()
            query = """
            SELECT M.title, M.release_date, M.vote_average, M.movie_id
            FROM playlist_movies AS PM
            JOIN movies AS M ON PM.movie_id = M.movie_id
         WHERE PM.playlist_id = %s;
            """
            cursor.execute(query, (playlist_id,))
            movies = cursor.fetchall()
            cursor.close()
            conn.close()
            return movies
        except Exception as e:
            print(f"Error fetching playlist movies: {e}")
            return []
        
    def delete_playlist(self, playlist_id):
        try:
            conn = psycopg2.connect(**self.db_config)
            cursor = conn.cursor()

            # Supprimer la playlist et ses films associés
            query = "DELETE FROM playlists WHERE playlist_id = %s;"
            cursor.execute(query, (playlist_id,))
            conn.commit()

            cursor.close()
            conn.close()
        except Exception as e:
            print(f"Error deleting playlist: {e}")
            raise


        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec_())
