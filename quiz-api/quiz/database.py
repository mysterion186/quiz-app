import sqlite3
import ast
import json
# from .models import Question
from .models import Question


PATH = "quiz.db"
def log_db(path) : 
    """Connectin to the database. Returns
    
    Keyword Argument :
    path -- str path to the db file
    """
    return sqlite3.connect(path)

def count_elements(table, path=PATH) :
    conn = log_db(path)
    result = conn.execute("Select count(*) from {0}".format(table))
    for row in result : 
        return row[0]
    conn.close()

def insert_question(question,path = PATH) : 
    """Function to insert a new question into the database.
    
    Keyword argument :
    question -- Question question object to instert into the database 
    path -- str path to the database file
    """
    conn = log_db(path)
    conn.execute('INSERT INTO question(id,title, text, image, position, possibleAnswers) VALUES (?,?,?,?,?,?)',(
                                                                                                                question.id,
                                                                                                                question.title, 
                                                                                                                question.text,
                                                                                                                question.image,
                                                                                                                question.position,
                                                                                                                json.dumps(question.possibleAnswers,ensure_ascii=False)
                                                                                                            ))
    conn.commit()
    conn.close()
    return

# récupérer l'image en base 64 et l'enregistrer sous forme de texte
def retrieve_one_question(value,key = "id", path = PATH) : 
    """Get all intel about a question with question's id.
    
    Keyword arguments : 
    value -- int question's id or position value
    key -- attribut we want to look for, (default is "id)
    path -- str path to the database
    """
    conn = log_db(path)
    data = conn.execute(f"SELECT * FROM question WHERE {key}='{value}'")
    question = None
    # only 1 loop, because position is an ID
    for row in data : 
        question = Question(
                            id = row[0],
                            title = row[1],
                            text = row[2],
                            image = row[3],
                            position = row[4],
                            possibleAnswers = row[5]
                        )
        print(question.possibleAnswers)
        # question.possibleAnswers = ast.literal_eval(question.possibleAnswers)
        question.possibleAnswers = json.loads(question.possibleAnswers)
    conn.close()
    return question

def retrieve_all_question(value, key = 'id', path = PATH):
    count = count_elements(path)
    questions = []
    for k in range(count):
        temp = retrieve_one_question(value, key, path)
        if temp != None : 
            questions.append(temp)
    return questions

def delete_question(rule) : 
    if rule == "all" :
        _delete_all_questions()
    else :
        _delete_id_question(rule)
    return

def _delete_id_question(question_id, path = PATH) : 
    conn = log_db(path)
    conn.execute(f"DELETE FROM question WHERE id='{question_id}'")
    conn.commit()
    conn.close()

def _delete_all_questions(path = PATH) : 
    conn = log_db(path)
    conn.execute(f"DELETE FROM question")
    conn.commit()
    conn.close()


def update_question(question, path = PATH) : 
    conn = log_db(path)
    conn.execute("""
            UPDATE question SET title = ?, 
                                text = ?,
                                image = ?,
                                position = ?,
                                possibleAnswers = ?
            WHERE id = ?
    """, (
        question.title,
        question.text,
        question.image,
        question.position,
        json.dumps(question.possibleAnswers, ensure_ascii=False),
        question.id
    ))
    conn.commit()
    conn.close()
