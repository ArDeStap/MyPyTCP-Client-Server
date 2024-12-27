import socket

def sendServerRequest(msg):
    # Шаг 1: Создание TCP/IP сокета
    server_address = ('127.0.0.1', 65432)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    # Шаг 2: Подключение к серверу
        try:
            
            client_socket.connect(server_address)
                # Шаг 3: Отправка и получение данных
            client_socket.sendall(message.encode())
                # Ожидание ответа от сервера
            data = client_socket.recv(131072)
            print(f"Received {data.decode()} from the server")

        except:
            client_socket.close()

msg = ''

while msg.lower() != "exit":
    msg = input('Your message to TCP SERVER ')
    sendServerRequest(msg)

