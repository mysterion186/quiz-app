import sqlite3
import ast
import json
# from .models import Question
from .models import Question


PATH = "quiz.db"
def log_db(path) : 
    """Connectin to the database.
    
    Args :
    path (str) : path to the db file. 
    
    Returns : 
    sqlite3.Connection : object to connect to the database.
    """
    return sqlite3.connect(path)

def count_elements(table, path=PATH) :
    """
    Count the number of elements in the given table.

    Args : 
    table (str) : table's name.
    path (str, optional) : path to the database. Default is PATH.

    Returns : 
    int : number of elements in the given table.
    """
    conn = log_db(path)
    result = conn.execute("Select count(*) from {0}".format(table))
    for row in result : 
        return row[0] + 1
    conn.close()

def insert_question(question,path = PATH) : 
    """Function to insert a new question into the database.
    
    Args :
    question (Question): Question to insert
    path (str, optional) : path to the database. Default is PATH.

    Returns : 
    None
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
    
    Args : 
    value (int) : value that we want to use to filter the sql select result
    key (str, optional) : attribut we want to look for in the filter. Default is 'id'.
    path (str, optional) : path to the db file. Default is PATH.
    
    Returns : 
    Union(Question, None) : return the object Question if something meets the criteria else None.
    """
    conn = log_db(path)
    data = conn.execute(f"SELECT * FROM question WHERE {key}='{value}' ORDER BY position")
    question = None
    # only 1 loop, because position and id are unique
    for row in data : 
        question = Question(
                            id = row[0],
                            title = row[1],
                            text = row[2],
                            image = row[3],
                            position = row[4],
                            possibleAnswers = row[5]
                        )
        question.possibleAnswers = json.loads(question.possibleAnswers)
    conn.close()
    return question

def retrieve_all_question(count, key = 'id', path = PATH):
    """
    Get all questions that goes from 0 to count.

    Args : 
    count (int) max number of questions to retrieve.
    key (str, optional) : value with what we want to retrieve the questions. Default is 'id'.
    path (str, optional) : path to the database file. Default is PATH.

    Returns : 
    list(Questions) : return all the Questions that met our research criteria. 
    """
    questions = []
    for k in range(count):
        temp = retrieve_one_question(k, key, path)
        if temp != None : 
            questions.append(temp)
    return questions

def delete_question(rule) : 
    """
    Delete either one or all the questions according to the given rule.

    Args :
    rule (Union[str, int]) : rule to follow. 

    Returns : 
    None
    """
    if rule == "all" :
        _delete_all_questions()
    else :
        _delete_id_question(rule)
    return

def _delete_id_question(question_id, path = PATH) : 
    """
    Delete one question according to the question's id.

    Args : 
    question_id (int) : question's id to delete.
    path (str, optional) : path to the db file. Default is PATH. 

    Returns : 
    None
    """
    question = retrieve_one_question(question_id)
    conn = log_db(path)
    conn.execute(f"DELETE FROM question WHERE id='{question_id}'")
    conn.commit()
    conn.close()
    question_number = count_elements("question")
    update_position(None, question,question_number, "delete")
    return

def _delete_all_questions(path = PATH) : 
    """
    Delete all questions from the question table.

    Args : 
    path (str, optional) : path to the db file. Default is PATH.

    Returns : 
    None
    """
    conn = log_db(path)
    conn.execute(f"DELETE FROM question")
    conn.commit()
    conn.close()
    return


def update_question(question, path = PATH) : 
    """
    update a question in the question table.

    Args : 
    question (Question) : question that we want to udpate inside de database.
    path (str, optional) : path to the db file. Default is PATH.

    Returns :
    None
    """
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
    return

def update_position(previous_pos, question, question_number,action_type) : 
    """
    Update questions position inside the question table.
    
    If the users delete a question all the following questions positions need to be updated.
    Same goes if a new question is added between position.

    previous_pos (Union[int, None]) : previous position of the question before the update. May be None in some case.
    question (Question) : Question to update.
    question_number (int) : Number of questions in total in the question table.
    action_type (str) : What action to perform. [update, insert, delete]
    """
    questions = retrieve_all_question(question_number)
    # update or insert the new question
    if action_type == "update" : 
        update_question(question)
    elif action_type == "insert" :
        insert_question(question)
    
    # loop over all the questions to update their position
    for elt in questions : 
        # in delete case, only the questions with position > the deleted question's position are updated (decrement 1)
        if action_type == "delete" :
            if elt.position >= question.position and elt.id != question.id : 
                elt.position -= 1
                update_question(elt)
            continue
        
        # in insert case, we only add 1 to question where their position is superior to the new question we want to insert
        elif action_type == "insert" :
            if elt.position >= question.position and elt.id != question.id :
                elt.position += 1 
                update_question(elt)
            continue
        
        # update case, find the position to know if we need to add 1 or decrement by 1
        if previous_pos >= question.position : 
            if (elt.position >= question.position and elt.position <= previous_pos) and elt.id != question.id :           
                elt.position += 1 
                update_question(elt)
        elif question.position > previous_pos :
            if (elt.position <= question.position and elt.position >= previous_pos) and elt.id != question.id :
                elt.position -= 1 
                update_question(elt)
    return

def get_correct_answer_pos(question) : 
    """
    Get to position of the correct answer in the list of possibleAnswers in a Question object.

    Args : 
    question (Question) : object for which we want the position of the correct answer.

    Returns : 
    int : position of the correct answer in the list of possibleAnswers.
    """
    answers = question.possibleAnswers
    count = 1
    for elt in answers :
        if not elt["isCorrect"] :
            count += 1 
        else : 
            break
    return count