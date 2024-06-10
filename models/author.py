import sqlite3

class Author:
    def __init__(self, id, name):
        self._id = id
        self.name = name
        self.save()

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        connection = sqlite3.connect('magazine.db')
        cursor = connection.cursor()
        cursor.execute('SELECT name FROM authors WHERE id = ?', (self._id,))
        name = cursor.fetchone()[0]
        connection.close()
        return name

    @name.setter
    def name(self, value):
        if isinstance(value, str) and len(value) > 0:
            self._name = value
        else:
            raise ValueError("Name must be a non-empty string")

    def save(self):
        connection = sqlite3.connect('magazine.db')
        cursor = connection.cursor()
        cursor.execute('INSERT INTO authors (name) VALUES (?)', (self._name,))
        self._id = cursor.lastrowid
        connection.commit()
        connection.close()

    def articles(self):
        connection = sqlite3.connect('magazine.db')
        cursor = connection.cursor()
        cursor.execute('''
            SELECT * FROM articles WHERE author_id = ?
        ''', (self._id,))
        articles = cursor.fetchall()
        connection.close()
        return articles

    def magazines(self):
        connection = sqlite3.connect('magazine.db')
        cursor = connection.cursor()
        cursor.execute('''
            SELECT DISTINCT magazines.* FROM magazines
            JOIN articles ON magazines.id = articles.magazine_id
            WHERE articles.author_id = ?
        ''', (self._id,))
        magazines = cursor.fetchall()
        connection.close()
        return magazines
