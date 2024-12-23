import os
import sys
import psycopg2
#from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget
               
class MovieDatabase:
        def __init__(self, database, user, host, password):
                self.conn = psycopg2.connect(database=database, user=user, host=host, password=password)
                #conn = psycopg2.connect(database="l3info_10", user="l3info_10", host="10.11.11.22", password="L3INFO_10")
                self.cursor = self.conn.cursor()

        def get_all_genres(self):
                self.cursor.execute("SELECT name FROM genres INNER JOIN movie_genres ON genres.genre_id = movie_genres.genre_id GROUP BY name ORDER BY count(*) DESC")  
                genres = self.cursor.fetchall()
                return [genre[0] for genre in genres]

        def get_all_keywords(self):
                self.cursor.execute("SELECT name FROM keywords INNER JOIN movie_keywords ON keywords.keyword_id = movie_keywords.keyword_id GROUP BY name ORDER BY count(*) DESC")
                keywords = self.cursor.fetchall()
                return [keys[0] for keys in keywords]
        
        def get_all_movies_name(self):
                self.cursor.execute("SELECT title FROM movies")
                movies = self.cursor.fetchall()
                return [movie[0] for movie in movies]
        
        def get_movies_by_genre(self, genre):
                if genre not in self.get_all_genres():
                        return []
                self.cursor.execute("SELECT title FROM (movies NATURAL JOIN movie_genres) AS a INNER JOIN genres ON a.genre_id = genres.genre_id WHERE name = %s", (genre,))
                movies = self.cursor.fetchall()
                return [movie[0] for movie in movies]
        
        # Return the list of movies that have all the genres in the list genres
        def get_movies_by_genre_list(self, genres):
                for genre in genres:
                        if genre not in self.get_all_genres():
                                return []
                self.cursor.execute("SELECT title FROM (movies m NATURAL JOIN movie_genres mg) JOIN genres g ON mg.genre_id = g.genre_id WHERE g.name IN %s GROUP BY m.movie_id, m.title HAVING count(DISTINCT g.genre_id) = %s;", (tuple(genres), len(genres)))
                movies = self.cursor.fetchall()
                return [movie[0] for movie in movies]

        def close(self):
                self.cursor.close()
                self.conn.close()
        
if __name__ == '__main__':
        # Connection
        db = MovieDatabase(database="mynewdb", user="arthur", host="localhost", password="")

        try:
                genres = db.get_all_genres()
                print(genres)
                keywords = db.get_all_keywords()
                print(keywords)
                movies = db.get_all_movies_name()
                print(movies)
                horror_movies = db.get_movies_by_genre("Horror")
                print(horror_movies)
                western_scifi_movies = db.get_movies_by_genre_list(["Western", "Science Fiction"])
                print(western_scifi_movies)
        finally:
                db.close()