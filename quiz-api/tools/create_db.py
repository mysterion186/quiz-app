import sqlite3

PATH = "quiz.db"
def log_db(path) : 
    """Connectin to the database. Returns
    
    Keyword Argument :
    path -- str path to the db file
    """
    return sqlite3.connect(path)

def create_question(path = PATH) :
    conn = log_db(path)
    c = conn.cursor()
    c.execute("create table question(id int primary key, title varchar, text varchar, image varchar, position int, possibleAnswers json);")
    conn.close()

def create_participation(path = PATH) :
    conn = log_db(path)
    conn.execute("CREATE TABLE participation (id INTEGER PRIMARY KEY AUTOINCREMENT, player_name TEXT NOT NULL, score INTEGER NOT NULL, date TEXT NOT NULL)")
    conn.close()
