#!/usr/bin/python3
import psutil

common_ports = {
    22: 'SSH',
    21: 'FTP',
    54: 'DNS',
    80: 'HTTP',
    443: 'HTTPS',
    25: 'SMTP',
    3306: 'MySQL'
}

def classify_port(port):
    return common_ports.get(port, 'Unknown')


# Diccionario de listas para agrupar conexiones por puerto
grouped_connections = {port: [] for port in common_ports}

def group_port(connection, port):
    if port in common_ports:
        grouped_connections[port].append(connection)

def print_formatted_connection(local_ip, local_port, remote_ip, remote_port, service_name):
    print(f"Local IP: {local_ip}")
    print(f"Local Port: {local_port}")
    print(f"Remote IP: {remote_ip}")
    print(f"Remote Port: {remote_port}")
    print(f"Service: {service_name}")
    print("\n")
##############################################################    
#for connection in psutil.net_connections():
def get_attributes(connection):
    try:
        local_ip = connection.laddr.ip
    except AttributeError:
        local_ip = "Unknown"

    try:
        local_port = connection.laddr.port
    except AttributeError:
        local_port = "Unknown"

    try:
        remote_ip = connection.raddr.ip
    except AttributeError:
        remote_ip = "Unknown"

    try:
        remote_port = connection.raddr.port
    except AttributeError:
        remote_port = "Unknown"

    service_name = classify_port(local_port)

    return local_ip, local_port, remote_ip, remote_port, service_name
# Ejemplo de uso en un bucle para todas las conexiones
for connection in psutil.net_connections():
    try:
        local_port = connection.laddr.port
    except AttributeError:
        local_port = None

    # Llamada a la función para agrupar la conexión según el puerto
    group_port(connection, local_port)


#SSH
def print_connection_by_port(port):
    ssh_connections = grouped_connections.get(port, [])
    if ssh_connections:
        service=classify_port(port)
        print(f"--------------------{service} Connections:")
        for connection in ssh_connections:
            print_formatted_connection(get_attributes(connection)[0],get_attributes(connection)[1],get_attributes(connection)[2],get_attributes(connection)[3], get_attributes(connection)[4] )


for port in common_ports:
    print_connection_by_port(port)
