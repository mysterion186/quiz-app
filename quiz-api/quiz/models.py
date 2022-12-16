import json


class Question() : 
    """
    Class that represents a question
    """
    def __init__(self,title,text,image,position,possibleAnswer) : 
        """Constructor to create a question object.
        
        Keyword Arguments : 
        title -- str question theme
        text -- str actual question
        image -- basecode 64 image that represents the question
        position -- int equivalent of the question id
        possibleAnswer -- list of dictionaries that contains possible answers
        """
        self.title = title 
        self.text = text
        self.image = image
        self.position = position
        self.possibleAnswer = possibleAnswer
    
    def toJson(self) : 
        """Method to serialize a question."""
        return json.dumps(self,default= lambda x : x.__dict__)


if __name__ == "__main__" : 
    question = Question(
        text = "Quelle est la couleur du cheval blanc d'Henry IV ?",
        title = "Histoire !",
        image ="falseb64imagecontent",
        position = 2, 
        possibleAnswer = [
            {
                "text": "Noir",
                "isCorrect": False 
            },
            {
                "text": "Gris",
                "isCorrect": False
            },
            {
                "text": "Blanc",
                "isCorrect": True
            },
            {
                "text": "La réponse D",
                "isCorrect": False
            }
        ]
    )
    print(question.toJson())
    import database
    conn = database.log_db(database.PATH)
    conn.close()
    database.insert_question(question)
    # result = database.retrieve_question("test",database.PATH)
    # print(result.toJson())


