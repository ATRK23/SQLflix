import sys
import psycopg2
import hashlib
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QLineEdit, QPushButton,
    QLabel, QMessageBox, QWidget, QDialog, QSpacerItem, QSizePolicy, QHBoxLayout, QCheckBox,
    QTableWidget, QTableWidgetItem, QGroupBox, QTabWidget
)
from PyQt5.QtGui import QPixmap, QFont, QIcon
from PyQt5.QtCore import Qt

# Configuration PostgreSQL 
DB_CONFIG = {
    'dbname': 'sqlflix',
    'user': 'postgres',
    'password': 'postgres',
    'host': 'localhost'
}

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("SQLFLIX - Sign in")
        self.setGeometry(300, 300, 400, 500)
        self.setWindowIcon(QIcon("icone.png"))

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        self.image_label = QLabel(self)
        self.pixmap = QPixmap("background.png")
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
        self.setWindowTitle("SQLFLIX - Homepage")
        self.setGeometry(100, 100, 800, 600)

        main_layout = QVBoxLayout()

        self.create_search_bar(main_layout)
        self.create_all_movies_section(main_layout)
        self.create_top_movies_section(main_layout)
        self.create_recommendations_section(main_layout)

        self.logout_button = QPushButton("Logout")
        self.logout_button.clicked.connect(self.logout)
        main_layout.addWidget(self.logout_button)

        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)

        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def create_search_bar(self, layout):
        search_layout = QHBoxLayout()

        self.search_input = QLineEdit(self)
        self.search_input.setPlaceholderText("Search for a movie...")
        self.search_input.textChanged.connect(self.filter_movies)

        search_layout.addWidget(self.search_input)
        layout.addLayout(search_layout)

    def filter_movies(self):
        search_text = self.search_input.text().lower()
        filtered_movies = self.get_filtered_movies(search_text)
        self.update_movie_table(filtered_movies)

    def create_all_movies_section(self, layout):
        all_movies_group = QGroupBox("Tous les Films")
        all_movies_layout = QVBoxLayout()

        self.all_movies_table = QTableWidget()
        self.all_movies_table.setColumnCount(4)
        self.all_movies_table.setHorizontalHeaderLabels(['Title', 'Genre', 'Year', 'Rating'])
        self.load_all_movies(self.all_movies_table)
        
        self.all_movies_table.cellDoubleClicked.connect(self.on_movie_double_clicked)

        all_movies_layout.addWidget(self.all_movies_table)
        all_movies_group.setLayout(all_movies_layout)
        layout.addWidget(all_movies_group)
    
    def create_top_movies_section(self, layout):
        top_movies_group = QGroupBox("Top 10 Films")
        top_movies_layout = QVBoxLayout()

        self.top_movies_table = QTableWidget()
        self.top_movies_table.setColumnCount(4)
        self.top_movies_table.setHorizontalHeaderLabels(['Title', 'Genre', 'Year', 'Rating'])
        self.load_top_movies(self.top_movies_table)
        
        self.top_movies_table.cellDoubleClicked.connect(self.on_movie_double_clicked)

        top_movies_layout.addWidget(self.top_movies_table)
        top_movies_group.setLayout(top_movies_layout)
        layout.addWidget(top_movies_group)

    def create_recommendations_section(self, layout):
        self.recommendations_group = QGroupBox("Recommandations")
        self.recommendations_layout = QVBoxLayout()

        self.recommendations_table = QTableWidget()
        self.recommendations_table.setColumnCount(4)
        self.recommendations_table.setHorizontalHeaderLabels(['Title', 'Genre', 'Release Date', 'Rating'])
        self.load_recommendations(self.recommendations_table)
        
        self.recommendations_table.cellDoubleClicked.connect(self.on_movie_double_clicked)

        self.recommendations_layout.addWidget(self.recommendations_table)
        self.recommendations_group.setLayout(self.recommendations_layout)
        layout.addWidget(self.recommendations_group)

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
        
    def open_movie_page(self, movie_id):
        movie_name = get_movie_name(movie_id)
        movie_year = get_movie_year(movie_id)

        # Vérifier si l'onglet existe déjà
        for index in range(self.tabs.count()):
            if self.tabs.tabText(index) == f"{movie_name} ({movie_year})":
                self.tabs.setCurrentIndex(index)  # Sélectionner l'onglet existant
                return

        # Créer un nouvel onglet pour le film
        movie_page = MoviePage(movie_id)
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
            self.open_movie_page(movie_id)

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
    def __init__(self, movie_id):
        super().__init__()

        self.movie_id = movie_id

        self.setWindowTitle(f"SQLFLIX - {get_movie_name(movie_id)} ({get_movie_year(movie_id)})")
        self.setGeometry(100, 100, 800, 600)

        
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec_())
