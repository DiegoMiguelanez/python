#!/usr/bin/python3.7
import mysql.connector
import paramiko
import re
"""
Este script en Python realiza la recopilación de datos crudos por SSH de los hostings compartidos mediante conexiones a servidores Plesk. 
Luego, parsea estos datos y los inserta o actualiza en una base de datos MySQL local. 
La información recopilada incluye el nombre del dominio, estado, descripción, servidor asociado, nombre del servidor y la marca "legacy". 
El script puede ser utilizado para mantener actualizada la información sobre los dominios hospedados en múltiples servidores Plesk en un entorno compartido.
"""
# Configuración de las conexiones SSH
conexiones_ssh = [
    #GL12 INSERTADO
   # {'hostname': '146.255.102.138', 'port': 22, 'username': 'root', 'password': '23X_lhq9', 'nombre_servidor': 'GL12', 'legacy':'MasMovil'},
    #GL13
    {'hostname': '195.114.216.238', 'port': 22, 'username': 'root', 'password': '&N45e7gq','nombre_servidor': 'GL13', 'legacy':'MasMovil'},
    #GL14 INSERTADO
  #  {'hostname': '146.255.102.144', 'port': 22, 'username': 'root', 'password': 'Fce8*n98','nombre_servidor': 'GL14', 'legacy':'MasMovil'},
    #GW11
    {'hostname': '5.56.56.91', 'port': 22, 'username': 'root', 'password': 'z43Fo1i?','nombre_servidor': 'GW11', 'legacy':'MasMovil'},
    #Inicia INSERTADO
    #{'hostname': '146.255.100.190', 'port': 22, 'username': 'root', 'password': 'ri8XIYZR','nombre_servidor': 'Inicia', 'legacy':'MasMovil'}
    #RPW7 -> Es un Windows
    #{'hostname': '146.255.102.253', 'port': 22, 'username': 'root', 'password': '51G1G**mm1gR','nombre_servidor': 'RPW7', 'legacy':'MasMovil'}

    # ... Agrega más máquinas según sea necesario
]

# Configuración de la conexión a la base de datos
conexion_bd = {
    'user': 'plesk',
    'password': 'itscumparplaneta',
    'host': 'localhost',
    'database': 'hostings_compartidos',
}

#1) FASE RECOPILAR DATOS EN CRUDO POR SSH DE LOS HOSTINGS COMPARTIDOS====================================================================================
######################

# Diccionario para almacenar el output por IP
output_por_ip = {}
output_por_ip_parseado = {}

# Iterar sobre cada conexión SSH
for conexion in conexiones_ssh:
    # Conectar por SSH y ejecutar el comando

    
    nombre_conexion = conexion.pop('nombre_servidor', None)
    legacy_conexion = conexion.pop('legacy', None)

    print(nombre_conexion)
    print(legacy_conexion)
    with paramiko.SSHClient() as ssh:
        #Sacamos de forma temporalmente los campos adicionales que impiden la conexion SSH
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(**conexion)
        print("Ha conectado correctamente...")
        # Obtener la IP de la conexión actual
        ip_actual = conexion['hostname']

        # Ejecutar el comando en la máquina remota(Limito 4 entradas para que no tarde mucho tiempo haciendo pruebas)
        #_, stdout, _: Este es un ejemplo de desempaquetado de tuplas. La función exec_command devuelve una tupla de tres elementos: 
        #la entrada estándar del proceso, la salida estándar del proceso y la salida de error estándar del proceso. 
        #Al utilizar _, se están descartando las entradas y salidas estándar. En este caso, solo nos interesa la salida estándar,
        # que se asigna a la variable stdout.
        _, stdout, _ = ssh.exec_command(
#            'count=0; '
            'for site in `plesk bin domain -l`; do '
            'echo $site; '
            'plesk bin domain -i $site | grep "Description for the administrator\|Domain status"; '
#            '  count=$((count+1)); '
#            '  if [ $count -eq 10]; then break; fi; '
            'done'
        )
        
        # Leer la salida del comando
        output = stdout.read().decode('utf-8')

        # Almacenar el output asociado a la IP
        output_por_ip[ip_actual] = output
    print(output)
    # Añadimos los acampos de nuevo al array
    conexion['nombre_servidor'] = nombre_conexion
    conexion['legacy'] = legacy_conexion
#2) FASE PARSEAR DATOS EN CRUDO PARA PODER EJECUTAR LAS QUERIES====================================================================================

#Funcion para parsear output del comado de Plesk
def parse_output(output):
    lines = output.strip().split('\n')
    grouped_lines = [lines[i:i+3] for i in range(0, len(lines), 3)]

    parsed_output = []

    for group in grouped_lines:
        if len(group) == 3:
            domain_name = group[0].strip()
            domain_status = group[1].strip().split(':')[1].strip()
            description = group[2].strip().split(':')[1].strip()
            parsed_output.append((domain_name, domain_status, description))
        else:
            return None

    return parsed_output


for conexion in conexiones_ssh:
    ip_actual = conexion['hostname']
    output_por_ip_parseado[ip_actual]=parse_output(output_por_ip[ip_actual])


#3) FASE INSERCION EN LA BBDD

# Conectar a la base de datos
conn = mysql.connector.connect(**conexion_bd)

# Crear un cursor para ejecutar consultas
cursor = conn.cursor()
print("Creando tabla...")
# Crear una tabla si no existe con primary key dominios para que cuando se hagan updates no dupliquen entradas
cursor.execute('''
    CREATE TABLE IF NOT EXISTS dominios (
        nombre VARCHAR(255) PRIMARY KEY,
        estado VARCHAR(255),
        descripcion TEXT,
        servidor VARCHAR(255),
        nombre_servidor VARCHAR(255),
        legacy VARCHAR(255)
    )
''')


    # Insertar o actualizar datos en la tabla
for conexion in conexiones_ssh:
    ip_actual = conexion['hostname']
    print("Insertando dominios")
    for dominio in output_por_ip_parseado[ip_actual]:
      
        # Añadir la IP actual como cuarto elemento a la tupla dominio
        dominio_con_ip = dominio + (ip_actual, conexion['nombre_servidor'], conexion['legacy'])
        cursor.execute('''
            INSERT INTO dominios (nombre, estado, descripcion, servidor, nombre_servidor, legacy)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
            estado=VALUES(estado), descripcion=VALUES(descripcion), servidor=VALUES(servidor),
            nombre_servidor=VALUES(nombre_servidor), legacy=VALUES(legacy);
        ''', dominio_con_ip)

    # Guardar los cambios y cerrar la conexión
conn.commit()
conn.close()
