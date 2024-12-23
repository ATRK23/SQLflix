import os
import sys
import psycopg2
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget

def connect_DB(self):
        self.conn = psycopg2.connect(database="myuniversitydb", user="mynabil", host="localhost", password="test")
        #self.conn = psycopg2.connect(database="l3info_10", user="l3info_10", host="10.11.11.22", password="L3INFO_10")
        self.cursor = self.conn.cursor()