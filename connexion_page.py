import sys
import psycopg2
import hashlib
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QLineEdit, QPushButton,
    QLabel, QMessageBox, QWidget, QDialog, QSpacerItem, QSizePolicy, QHBoxLayout, QCheckBox
)
from PyQt5.QtGui import QPixmap, QFont, QIcon
from PyQt5.QtCore import Qt
from home_page import HomePage

# Configuration PostgreSQL 
# Put YOUR ids
DB_CONFIG = {
    'dbname': 'sqlflix',
    'user': 'postgres',
    'password': 'database12@',
    'host': 'localhost',
    'port': '5432'
}


class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Window configuration
        self.setWindowTitle("SQLFLIX - Sign in")
        self.setGeometry(300, 300, 400, 500)

        # Définir l'icône de la fenêtre
        self.setWindowIcon(QIcon("icone.png"))

        # Central Widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Principal Layout
        self.layout = QVBoxLayout()

        # Image add (Label)
        self.image_label = QLabel(self)
        self.pixmap = QPixmap("background.png")
        self.image_label.setPixmap(self.pixmap)
        self.image_label.setScaledContents(True)
        self.layout.addWidget(self.image_label)

        # Adding a title
        title_label = QLabel("Connection to SQLFLIX", self)
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(title_label)

        # Input fields
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.username_input.setStyleSheet("padding: 10px; border-radius: 5px; border: 1px solid #ccc;")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet("padding: 10px; border-radius: 5px; border: 1px solid #ccc;")
        self.layout.addWidget(self.username_input)
        self.layout.addWidget(self.password_input)

        # Check to show:hide the password
        self.show_password_checkbox = QCheckBox("Show the password")
        self.show_password_checkbox.stateChanged.connect(self.toggle_password_visibility)
        self.layout.addWidget(self.show_password_checkbox)

        # Buttons
        self.login_button = QPushButton("Sign in")
        self.signup_button = QPushButton("Sign up")
        self.login_button.setStyleSheet(
            "padding: 10px 20px; border-radius: 5px; background-color: #0078d7; color: white;"
        )
        self.signup_button.setStyleSheet(
            "padding: 10px 20px; border-radius: 5px; background-color: #5c5c5c; color: white;"
        )

        # Buttons add
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.login_button)
        button_layout.addWidget(self.signup_button)
        self.layout.addLayout(button_layout)

        # Connect the buttons to actions
        self.password_input.returnPressed.connect(self.authenticate)
        self.login_button.clicked.connect(self.authenticate)
        self.signup_button.clicked.connect(self.open_signup_window)

        # Apply the layout
        self.central_widget.setLayout(self.layout)

    def resizeEvent(self, event):
        """Adapts the size of the image when the window is resized"""
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
            self.close()  # Close the connection window
            self.open_home_page()
        else:
            QMessageBox.warning(self, "Error", "Invalid username or password.")
    
    def open_home_page(self):
        username = self.username_input.text()
        self.home_page = HomePage(username)  # Crée une instance de la page d'accueil
        self.home_page.show()  # Affiche la page d'accueil
        self.close()
    
    def toggle_password_visibility(self):
        """
        Showing or hiding the password
        """
        if self.show_password_checkbox.isChecked():
            self.password_input.setEchoMode(QLineEdit.Normal)  # show the text
        else:
            self.password_input.setEchoMode(QLineEdit.Password)  # hide the text

    def check_credentials(self, username, password):
        try:
            conn = psycopg2.connect(**DB_CONFIG)
            cursor = conn.cursor()

            # Hashing the password entered
            hashed_password = hashlib.sha256(password.encode()).hexdigest()

            # Query to verify the informations
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

    def open_main_window(self):
        QMessageBox.information(self, "Welcome", "Welcome to SQLFLIX !")


class SignupWindow(QDialog):
    def __init__(self):
        super().__init__()

        # Window configuration 
        self.setWindowTitle("SQLFLIX - Sign up")
        self.setGeometry(400, 300, 350, 400)

        # Principal layout
        self.layout = QVBoxLayout()

        # Title
        title_label = QLabel("Create an account")
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(title_label)

        # Sign up fields
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

        # Sign up button
        self.signup_button = QPushButton("Sign up")
        self.signup_button.setStyleSheet(
            "padding: 10px 20px; border-radius: 5px; background-color: #0078d7; color: white;"
        )
        self.signup_button.clicked.connect(self.register_user)

        self.layout.addWidget(self.signup_button, alignment=Qt.AlignCenter)

        # Apply the layout
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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec_())
