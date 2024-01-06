#!/usr/bin/python
from git import Repo
import os
import paramiko
import sys

# Definimos la ruta de instalación
ruta_instalacion = '/usr/diego-utils'

# Verificar si se proporcionó la IP destino como argumento
if len(sys.argv) < 2:
    print("Por favor, comparta la IP destino como argumento para este script")
    sys.exit(1)  # Terminar el programa con un código de error



remote_host = sys.argv[1]
remote_user = 'root'
remote_password = 'Virtual18'

# Definimos el repositorio 
repo_url = "https://github.com/DiegoMiguelanez/python.git"

# Creamos una conexión SSH
ssh_client = paramiko.SSHClient()

# Acepta automáticamente cualquier clave de host desconocida y la almacena localmente.(Asi no tendremos que aceptar el nuevo host como confiable)
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# Nos conectamos
ssh_client.connect(remote_host, username=remote_user, password=remote_password)

# Nos aseguramos de que exista la ruta en la máquina remota, sino la creamos
ssh_client.exec_command(f'mkdir -p {ruta_instalacion}')

# Clonamos el repositorio en la máquina remota
git_command = f'git clone {repo_url} {ruta_instalacion}'
ssh_client.exec_command(git_command)

# Cerramos la conexión SSH
ssh_client.close()


