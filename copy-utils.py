#!/usr/bin/python
from git import Repo
import shutil
import os

#Definimos ruta de instalacion
ruta_instalacion='/usr/diego-utils'

#Definimos el repositorio 
repo_url = "https://github.com/DiegoMiguelanez/python.git"


#Nos aseguramos de que exista la ruta, sino la creamos
if not os.path.exists(ruta_instalacion):
    os.mkdir(ruta_instalacion)

#Usamos Repo.clone_from tal y como encontramos en la documentacion oficial
#https://gitpython.readthedocs.io/en/stable/quickstart.html
repo = Repo.clone_from(repo_url, ruta_instalacion)
