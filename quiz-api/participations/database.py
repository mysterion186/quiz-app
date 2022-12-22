import sqlite3
import ast
import json
from .models import Participation


PATH = "quiz.db"
def log_db(path) : 
    """Connectin to the database. Returns
    
    Keyword Argument :
    path -- str path to the db file
    """
    return sqlite3.connect(path)

def delete_participation(path = PATH) : 
    conn = log_db(path)
    conn.execute("DELETE FROM participation")
    conn.commit()
    conn.close()
    return