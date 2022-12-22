import json


class Participation():
    """
    Class that represents a participation
    """
    def __init__(self,player_name,answers,date):
        self.player_name = player_name
        self.answers = answers
        self.date = date
        self.score = None

    def toJson(self) :
        """Method to serialize a participation."""
        return json.dumps(self,default= lambda x : x.__dict__, ensure_ascii = False)