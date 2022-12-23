import json


class Participation():
    """
    Class that represents a participation
    """
    def __init__(self,playerName,score,date):
        self.playerName = playerName
        self.date = date
        self.score = score

    def toJson(self) :
        """Method to serialize a participation."""
        return json.dumps(self,default= lambda x : x.__dict__, ensure_ascii = False)