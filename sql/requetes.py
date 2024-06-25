import sqlite3
from sqlite3 import Error

from pydantic import BaseModel
from sql import init
from fastapi import HTTPException

#requete SELECT DATA
def fetchLink():
    #on verifie l'initialisation de la bdd (database)
    bdd = init.db_init()
    print(f'bdd apres avoir été init : {bdd}')
    # verif si none
    if bdd is None: 
        raise HTTPException(status_code=500, detail=f'Erreur initialisation base de donnees voir fichier init.py function db_init()')
    
    #si not none
    try : 
        req = bdd.cursor()
        req.execute('SELECT * FROM link_api')
        data = req.fetchall()
        print(data)
        datas = ''
        for row in data:
            datas = row[1]
        return datas
    
    except Error as e:
        raise HTTPException(status_code=400, detail=f'Erreur lors de la recuperation link api {e}')
    
    finally: 
        if bdd:
            req.close()
            bdd.close()

#requete INSERT DATA

def insertLink(link):
    #on return bdd de init
    bdd = init.db_init()

    # verif si none
    if bdd is None: 
        raise HTTPException(status_code=500, detail=f'Erreur initialisation base de donnees voir fichier init.py function db_init()')
    
    #si not none
    try : 
        print(f'avant post insert link : {link}')
        req = bdd.cursor()
        datas = (link,)

        #on recup la table
        req.execute('SELECT * FROM link_api')
        data = req.fetchone()
        if data is None: #si table est vide
            req.execute('INSERT INTO link_api(link_name) VALUES (?)', datas )
            bdd.commit()
            return {'message ':  'Link API enregistré avec succès'}
        else: #si table déjà contenu on update unique
            updateLink(link)
            return {'message ':  'Link API Update avec succès'}
    
    except Error as e:
        raise HTTPException(status_code=400, detail=f'Erreur lors de l\'insertion du link api {e}')
    
    finally: 
        if bdd:
            req.close()
            bdd.close()


#requete UPDATE DATA
def updateLink(link):
    #on return bdd de init
    bdd = init.db_init()

    # verif si none
    if bdd is None: 
        raise HTTPException(status_code=500, detail=f'Erreur initialisation base de donnees voir fichier init.py function db_init()')
    
    #si not none
    try : 
        print(f'avant post UPDATE link : {link}')
        req = bdd.cursor()
        #on update tjr la ligne 1
        id = 1
        datas = (link, id)
        req.execute('UPDATE link_api SET link_name = ? WHERE id = ?', datas )
        bdd.commit()

        if bdd.commit() is None:
            return {'message ':  'Link API update avec succès'}     

    
    except Error as e:
        raise HTTPException(status_code=400, detail=f'Erreur lors de l\'insertion du link api {e}')
    
    finally: 
        if bdd:
            req.close()
            bdd.close()

#requete DELETE DATA
def deleteLink(id):
    #on return bdd de init
    bdd = init.db_init()

    # verif si none
    if bdd is None: 
        raise HTTPException(status_code=500, detail=f'Erreur initialisation base de donnees voir fichier init.py function db_init()')
    
    #si not none
    try : 
        req = bdd.cursor()

        datas = (id,)
        req.execute('DELETE from link_api WHERE id = ?', datas )
        bdd.commit()

        if bdd.commit() is None:
            return {'message ':  'Link API DELETE avec succès'}
    
    except Error as e:
        raise HTTPException(status_code=400, detail=f'Erreur lors de l\'insertion du link api {e}')
    
    finally: 
        if bdd:
            req.close()
            bdd.close()
    return
