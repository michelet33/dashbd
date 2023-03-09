# FTP Server

## Requirement
Need to install library pyftpdlib

## How to installation pyftpdlib
> pip install pyftpdlib

## Créer les clefs
Exécuter la commande suivante pour créer les fichiers server.key et server.crt :
> openssl req -new -x509 -nodes -out server.crt -keyout server.key

## créer le fichier .pem
Copiez/collez le contenu des deux fichiers dans un seul fichier:
keycert.pem


## Lancer le server
> python main.py
