'''

import mysql.connector

#on défini les informations de connexion
host = '192.168.1.38'
user = 'root'
password = 'nathalia974'
database = 'api_flutter_woocommerce'
port= '3406'

#on etabli la connexion 
try :
    #connexion à la base de données
    db = mysql.connector.connect(
        host = host,
        user = user,
        password = password,
        database = database,
        port = port,
    )

except mysql.connector.Error as error :
    print(f'Erreur : {error}')
'''