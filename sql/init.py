import sqlite3
from sqlite3 import Error
from sql import connect

# function init bdd et creation table
def db_init():
    
    #on recup bdd
    bdd = connect.db_connect()

    #on ecoute return
    if bdd is not None:
        try : 
            req = bdd.cursor()

            #on verifie que la table link_api est not None
            req.execute("SELECT name FROM sqlite_master WHERE type='table' AND name = 'link_api' ")
            data = req.fetchone() #none si non existant - not None si existant

            if data is None:
                #data is None (non existant) on creer la table 
                sql = '''
                    CREATE TABLE link_api(
                    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    link_name TEXT NOT NULL
                    )
                    '''
                req.execute(sql)
                bdd.commit()
            else:
                print('Table user déjà creer')

        except Error as e:
            print(f'erreur lors de la creation de la table link_api - erreur : {e}')
            return None
        
        finally :
            if bdd:
                print('bdd return ok!')
                return bdd