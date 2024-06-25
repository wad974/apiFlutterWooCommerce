from pydantic import BaseModel

class Login(BaseModel):
    def __init__(self, utilisateur_id, utilisateur_name, utilisateur_date):
        self.utilisateur_id : utilisateur_id
        self.utilisateur_name : utilisateur_name
        self.utilisateur_date : utilisateur_date