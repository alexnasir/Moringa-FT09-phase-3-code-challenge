from database.connection import get_db_connection

class Author:
    def __init__(self,id, name):
        self.id = id
        self._name = name

        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO authors (name) VALUES (?);", (self._name,))
        self._id = cursor.lastrowid
        connection.commit()
        connection.close()

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        if not isinstance(value, int):
            raise ValueError("ID must be an integer.")
        self._id = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if hasattr(self,'_name'):
            raise AttributeError("Name cannot be changed after author's instantied")
        if not isinstance(value, str):
            raise TypeError("name must be a string")
        self._name = value
        if len(value) < 0:
            raise ValueError("name must be longer than 0 characters")
        self._name = value

    def articles(self):
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('''
        SELECT title FROM articles WHERE author_id = ?;
        ''', (self._id,))
        articles = cursor.fetchall()
        connection.close()
        return [article[0] for article in articles]

    def magazines(self):
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('''
        SELECT DISTINCT m.name FROM magazines m
        INNER JOIN articles a ON m.id = a.magazine_id
        WHERE a.author_id = ?;
        ''', (self._id,))
        magazines = cursor.fetchall()
        connection.close()
        return [magazine[0] for magazine in magazines]

    def __repr__(self):
        return f"Author(id={self._id}, name={self._name})"