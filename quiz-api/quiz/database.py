import sqlite3
from .models import Question


PATH = "quiz.db"
def log_db(path) : 
    """Connectin to the database. Returns
    
    Keyword Argument :
    path -- str path to the db file
    """
    return sqlite3.connect(path)


def insert_question(question,path = PATH) : 
    """Function to insert a new question into the database.
    
    Keyword argument :
    question -- Question question object to instert into the database 
    path -- str path to the database file
    """
    conn = log_db(path)
    conn.execute('INSERT INTO question(title, text, image, position, possibleAnswer) VALUES ("{}","{}","{}",{},"{}")'.format(
                                                                                                                                question.title, 
                                                                                                                                question.text,
                                                                                                                                question.image,
                                                                                                                                question.position,
                                                                                                                                question.possibleAnswer
                                                                                                                            ))
    conn.commit()
    conn.close()
    return

# récupérer l'image en base 64 et l'enregistrer sous forme de texte
def retrieve_question(question_position, path = PATH) : 
    """Get all intel about a question with question's id.
    
    Keyword arguments : 
    question_position -- int question's id
    path -- str path to the database
    """
    conn = log_db(path)
    data = conn.execute(f"SELECT * FROM question WHERE title='{question_position}'")
    question = None
    # only 1 loop, because position is an ID
    for row in data : 
        question = Question(row[0])
    return question