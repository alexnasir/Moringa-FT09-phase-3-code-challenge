from database.connection import Connection

class Author:
    def __init__(self, id, name):
          if not isinstance(id, int):
            raise ValueError("ID must be an integer.")
          
          if not isinstance(name, str) or len(name) == 0:
            raise ValueError("Names must be longer than 0 characters")
          
          self.id = id
          self.name = name

    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, value):
        self._id = value

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
         if not isinstance(value, str) or len(value) == 0:
            raise ValueError("Names must be longer than 0 characters")
         self._name = value
         
         #raise AttributeError("Cannot modify name after instantiation")
    
    def articles(self):
     query = """
        SELECT articles.id, articles.title, articles.content, authors.name 
        FROM articles
        JOIN authors ON articles.author_id = authors.id
        WHERE authors.id = ?;
     """
     return Connection.get_db_connection().execute(query, (self.id,)).fetchall()
    
    def magazines(self):
        query = """
            SELECT DISTINCT m.* 
            FROM magazines m
            JOIN articles a ON a.magazine_id = m.id
            WHERE a.author_id = ?;
        """
        return Connection.get_db_connection().execute(query, (self.id,)).fetchall()

        
    
