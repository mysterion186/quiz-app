import sqlite3
import ast
import json
from .models import Participation
from datetime import datetime

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

def insert_participation(participation,path = PATH) :
    conn = log_db(path)
    conn.execute("INSERT INTO participation(player_name, score, date) VALUES (?,?,?)", (
                                                                                        participation.playerName,
                                                                                        participation.score,
                                                                                        participation.date
                                                                                    ))
    conn.commit()
    conn.close()

def retrieve_all_participations(path = PATH):
    conn = log_db(path)
    data = conn.execute("SELECT * FROM participation ORDER BY score DESC")
    participations = []
    for row in data : 
        print(row)
        participation = Participation(
            playerName = row[1],
            score = row[2],
            date = row[3]
        )
        participations.append(json.loads(participation.toJson()))
    print(participations)
    return participations