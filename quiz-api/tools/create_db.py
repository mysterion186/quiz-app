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
    c.execute("create table question(id int primary key, title varchar(255), text varchar(255), image varchar(255), position int, possibleAnswers json);")
    conn.close()
