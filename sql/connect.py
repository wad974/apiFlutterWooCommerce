import sqlite3
from sqlite3 import Error

#function SQL connexion et creation de base de donnes sqlite
def db_connect():
    try: 
        #nom bdd
        bdd = sqlite3.connect('db_api')
    
    except Error as e:
        print(f'Echec lors de la creation base de donnees erreur {e}')
        return None

    finally:
        #si pas d'erreur
        return bdd