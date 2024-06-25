from fastapi import FastAPI, HTTPException
import requests
import uvicorn
import datetime
from pydantic import BaseModel
import json

#import fichier
from wooAuth import auth as log
from models import loginModel
from sql import init, bdd, requetes

#import sqlite pour bdd interne
import sqlite3
from sqlite3 import Error

app = FastAPI()

#init bdd lors du démarrage
init.db_init()
#
#
#
#getLinkApi
@app.get('/fetchlinkApi')
async def getLinkApi():
    #init bdd depuis requete
    data = requetes.fetchLink()
    #on retourne data
    return {'link' : data}
#
#
#
#insertLinkApi
class LinkName(BaseModel):
    name : str

@app.post('/postlinkapi')
async def postLinkApi(link : LinkName):
    #requetes.insertLink(link.name)
    print(f'insert link : {link.name}')
    message = requetes.insertLink(link.name)
    print(f'il y a quoi dans message:{message}')
    return message
#
#
#
#UpdateLinkApi

@app.put('/updatelinkapi')
async def updateLinkApi(link : LinkName):
    #requetes.updateLink(link.name)
    print(f'update link : {link.name}')
    message = requetes.updateLink(link.name)
    print(f'il y a quoi dans message:{message}')
    return message
#
#
#
#deleteLinkApi
class DeleteLink(BaseModel):
    id : int

@app.delete('/deletelinkapi')
async def deleteLinkApi(link : DeleteLink):
    #requetes.updateLink(link.name)
    print(f'delete link : {link.id}')
    message = requetes.deleteLink(link.id)
    print(f'il y a quoi dans message:{message}')
    return message
#
#
#
#requete pour recuperé tous les orders sur wooCommerce /allcommandes
@app.get('/allcommandes')
async def getAllOrders(per_page: int = 100):
    #on init liste vide
    data = []
    page = 1
    
    #boucle tant que
    while True:

        #on recup connexion
        response = requests.get(
            #f'https://woo.jcwad.re/wp-json/wc/v3/orders',
            log.link,
            params={
                'consumer_key':log.consumer_key,
                'consumer_secret':log.consumer_secret,
                'per_page' : per_page,
                'page' : page,
                'order' : 'desc',
            }
        )

        if response.status_code == 200 : 
            req = response.json()
            
            #on arrete la boucle s'il n'y a plus de nouvelle commandes
            if not req :
                break

            for row in req:
                data.append(
                    {
                        'id' : row['id'],
                        'nom' : row['billing']['first_name'],
                        'prenom' : row['billing']['last_name'],
                        'date' :  row ['date_created'] ,
                        'adresse' : row['shipping']['address_1']+' '+row['shipping']['address_2']+ ' ' +row['shipping']['postcode']+ ' ' + row['shipping']['city'],
                        'status': row['status'],
                    }
                )
            page += 1 # on ajoute des pages
        
        else:
            raise HTTPException(status_code=response.status_code, detail=response.text)
    
    return data
#
#
#
#requete pour recuperé tous les orders sur wooCommerce /commandes
@app.get('/commandes')
async def getOrders():
    #on init liste vide
    data = []
    print(f'nouveau lien : {log.link}')
    #on recup connexion woocommerce orders
    response = requests.get(
            #f'https://woo.jcwad.re/wp-json/wc/v3/orders',
            log.link,
            params={
                'consumer_key':log.consumer_key,
                'consumer_secret':log.consumer_secret,
                'order' : 'desc',
            }
        )

    if response.status_code == 200 : 
            req = response.json()
            # print(f'la liste commandes : {req}')
            id = ''
            for row in req:
                # on recup shipping
                shipping_methods = ', '.join(ship['method_title'] for ship in row['shipping_lines'])

                data.append(
                    {
                        'id' : row['id'],
                        'nom' : row['billing']['first_name'],
                        'prenom' : row['billing']['last_name'],
                        'date' :  row ['date_created'] ,
                        'adresse' : row['shipping']['address_1']+' '+row['shipping']['address_2']+ ' ' +row['shipping']['postcode']+ ' ' + row['shipping']['city'],
                        'status': row['status'],
                        'shipping' : shipping_methods
                    }
                )
                
        
    else:
            raise HTTPException(status_code=response.status_code, detail=response.text)
    
    return data
#
#
#
##update Status woocommerce
class Status(BaseModel):
    status : str
    id : int

@app.put('/updateStatus')
async def update_status(status : Status):
    print(status.status)
    print(status.id)
    
    #base_url = "https://woo.jcwad.re/wp-json/wc/v3/orders/"
    base_url = log.link
    order_id = status.id
    
    order_status = status.status
    
    url = f'{base_url}{order_id}'
    
    data_status = {
        'status' : order_status
    }
    
    response = requests.put(
        url, 
        auth=(log.consumer_key, log.consumer_secret), 
        data=json.dumps(data_status),
        headers={"Content-Type" : "application/json"}
        )
    
    if response.status_code == 200 :
        print('Statut de la commande mis à jour avec succès.')
        return {'message': 'Statut de la commande mis a jour avec succes.'}, 200
    else : 
        print(f'erreur lors de la mise a jour de la commande : {response.status_code} ')
        print(response.json())
#
#
#
#main
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=1111)