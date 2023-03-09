# FTP Server

## Requirement
Need to install library pyftpdlib

## How to installation pyftpdlib
> pip install pyftpdlib

## How to install FTP server
> python -m pyftpdlib -w --user=userftp --password=pwdftp 

or 

> python -m pyftpdlib -i 192.168.1.129 -w --user=userftp --password=pwdftp 

## Test FTP
Use application like FileZilla to test connexion.

Exemple lien fichier:  
ftp://userftp:userpwd@192.168.1.129:2121/update-image-4.5.1r10a-rc6.swu
ftp://userftp:userpwd@192.168.1.129:2121/update-image-4.4.3r2a.swu