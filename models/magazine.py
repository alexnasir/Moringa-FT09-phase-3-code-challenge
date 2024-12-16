from database.connection import Connection

class Magazine:
    def __init__(self, id, name, category):
        if not isinstance(name, str) or not (2 <= len(name) <= 16):
            raise ValueError("Name must be a string between 2 and 16 characters.")
         
        if not isinstance(category, str) or len(category) == 0:
            raise ValueError("Category must be a non-empty string.")
         
        self._id = id
        self.name = name
        self._category = category  

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or not (2 <= len(value) <= 16):
            raise ValueError("Name must be a string between 2 and 16 characters.")
        self._name = value

    @property
    def category(self):
        query = "SELECT category FROM magazines WHERE id = ?;"
        result = Connection.get_db_connection().execute(query, (self._id,)).fetchone()
        return result[0] if result else None

    @category.setter
    def category(self, value):
        if not isinstance(value, str) or len(value) == 0:
            raise ValueError("Category must be a non-empty string.")
        
        query = "UPDATE magazines SET category = ? WHERE id = ?;"
        Connection.get_db_connection().execute(query, (value, self._id))
        self._category = value

    def articles(self):
        query = "SELECT * FROM articles WHERE magazine_id = ?;"
        return Connection.get_db_connection().execute(query, (self.id,)).fetchall()

    def contributors(self):
        query = """
            SELECT DISTINCT authors.* 
            FROM authors 
            JOIN articles ON authors.id = articles.author_id
            WHERE articles.magazine_id = ?;
        """
        return Connection.get_db_connection().execute(query, (self.id,)).fetchall()

    def article_titles(self):
        query = "SELECT title FROM articles WHERE magazine_id = ?;"
        titles = Connection.get_db_connection().execute(query, (self.id,)).fetchall()
        return [title[0] for title in titles] if titles else None

    def contributing_authors(self):
        query = """
            SELECT authors.*, COUNT(articles.id) AS article_count 
            FROM authors
            JOIN articles ON authors.id = articles.author_id
            WHERE articles.magazine_id = ?
            GROUP BY authors.id
            HAVING article_count > 2;
        """
        return Connection.get_db_connection().execute(query, (self.id,)).fetchall()
