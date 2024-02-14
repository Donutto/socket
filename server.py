import socket
import threading

clients = []

def handle_client(client_socket, client_address):
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                print(f'Client {client_address} disconnected')
                clients.remove(client_socket)
                client_socket.close()
                break

            for client in clients:
                if client != client_socket:
                    status_code = 200
                    status_phrase = "OK"
                    status_line = f"HTTP/1.1 {status_code} {status_phrase} {data}"
                    client.sendall(status_line.encode())

        except ConnectionError as e:
            if client_socket in clients:
                clients.remove(client_socket)
                client_socket.close()
                print("Clients disconnected")
            break
        except Exception as e:
            print(f"Error: {e}")
            break



with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    HOST = '127.0.0.1'
    PORT = 65432

    server_socket.bind((HOST, PORT))

    server_socket.listen()
    print('Server is listening...')

    while True:
        client_socket, client_address = server_socket.accept()
        print(f'Connected to {client_address}')

        clients.append(client_socket)

        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()
