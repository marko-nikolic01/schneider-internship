import socket
from utils.messages import invalid_arguments, received_request
from utils.validation import is_float
from ports import DIVIDE_PORT
from hosts import HOST


def divide(a: float, b: float):
    return a / b

def validate_command(tokens):
    return tokens[0] == "DIV" and is_float(tokens[1]) and is_float(tokens[2])

def server_loop():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((HOST, DIVIDE_PORT))
        server.listen()
        connection, address = server.accept()
        with connection:
            print(received_request(address))
            while True:
                data = connection.recv(1024)
                if not data:
                    connection.sendall(invalid_arguments)
                    break

                tokens = data.decode().split()

                if not validate_command(tokens):
                    connection.sendall(invalid_arguments)
                    break

                num1 = float(tokens[1])
                num2 = float(tokens[2])

                result = divide(num1, num2)
                
                connection.sendall(bytes(str(result).encode()))


while True:
    server_loop()
