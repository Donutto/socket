import socket
import threading

def receive_messages(client_socket):
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break
            print(data.decode())

        except Exception as e:
            break

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    HOST = '127.0.0.1'
    PORT = 65432

    client_socket.connect((HOST, PORT))

    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    while True:
        message = input()
        if message == 'exit':
            client_socket.close()
            break
        else:
            client_socket.sendall(message.encode())