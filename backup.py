#!/usr/bin/python3
from datetime import datetime
import os
import sys
import shutil

ruta_backups='/var/backup'

def agregar_fecha_al_nombre(nombre_archivo):
    nombre_base, extension = os.path.splitext(nombre_archivo)
    now = datetime.now()
    hora_formateada = now.strftime("%Y%m%d%H%M_%S")

    return f"{nombre_base}_{hora_formateada}{extension}"

def copiar_archivo_ruta_backups(origen, destino, nuevo_nombre_archivo):
    # Combina el nombre del archivo nuevo con la ruta de destino
    ruta_destino = os.path.join(destino, nuevo_nombre_archivo)
     # Copia el archivo desde la ubicación de origen a la ubicación de destino con el nuevo nombre
    shutil.copy2(origen, ruta_destino)


if __name__ == "__main__":
    # Verifica si se proporciona al menos un argumento (el nombre del archivo)
    if len(sys.argv) < 2:
        print("Se requiere el nombre de un archivo como argumento.")
    else:
        # Obtiene el nombre del archivo del primer argumento
        nombre_archivo = sys.argv[1]

        #Si no existe la ruta para backups la creamos
        if not os.path.exists(ruta_backups):
            os.makedirs(ruta_backups)

        #Si existe la ruta para backups, es un directorio y si el archivo existe aplicamos la funcion de copiar archivo con fecha y hora formateada
        if os.path.exists(ruta_backups) and os.path.isdir(ruta_backups) and os.path.exists(nombre_archivo):
            copiar_archivo_ruta_backups(nombre_archivo, ruta_backups, agregar_fecha_al_nombre(nombre_archivo))

        else:
            print("No existe la ruta a guardar o bien el archivo compartido como argumento")
