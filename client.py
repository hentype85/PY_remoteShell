import socket
import os

try:
    # variables de entorno del servidor
    host = os.getenv('SERVER_HOST')
    port = int(os.getenv('SERVER_PORT'))
except (Exception, ValueError, TypeError):
    print("Error in server environment variables")

# direccion del servidor
server_address = (host, port)
client_socket = socket.socket()

try:
    # conectar al servidor
    client_socket.connect(server_address)

    while True:
        # ingresar comando
        comando_enviar = input(">> ")

        if not comando_enviar:
            continue

        if comando_enviar.lower() == 'cls':
            os.system('cls')
            continue

        elif comando_enviar.lower() == 'exit':
            client_socket.send(comando_enviar.encode())
            break

        elif comando_enviar.split(" ")[0] == 'download':
            try:
                # enviar comando al servidor
                client_socket.send(comando_enviar.encode())

                # recibir tamaño del archivo
                file_size = int(client_socket.recv(1024).decode())

                # enviar confirmacion al servidor
                client_socket.send("OK".encode())

                # crear directorio si no existe en la ruta actual
                save_folder = os.path.join(os.getcwd(), 'downloads')
                if not os.path.exists(save_folder):
                    os.makedirs(save_folder)

                # recibir el archivo
                file_name = comando_enviar.split(" ")[1]
                file_path = os.path.join(save_folder, file_name)
                with open(file_path, 'wb') as fd:
                    while file_size > 0:
                        # recibir datos y escribir archivo
                        data = client_socket.recv(1024)
                        fd.write(data)
                        # actualizar el tamaño del archivo
                        file_size -= len(data)

            except Exception as e:
                print(e)

        else:
            # enviar comando al servidor
            client_socket.send(comando_enviar.encode())

            # recibir y mostrar respuesta del servidor
            respuesta = client_socket.recv(4096)
            print(respuesta.decode())

except Exception as e:
    print(e)

finally:
    # cerrar el socket
    client_socket.close()
