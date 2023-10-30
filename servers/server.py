import socket
from utils.messages import invalid_arguments, received_request
from utils.validation import is_float, is_arithmetic_operation
from ports import *
from hosts import HOST


def validate_command(tokens):
    if len(tokens) % 2 != 1:
        return False
    for i, token in enumerate(tokens):
        r = i % 2
        if r == 0:
            if not is_float(token):
                return False
        elif r == 1:
            if not is_arithmetic_operation(token):
                return False
    return True

def calculate_next(num1, num2, operation):
    port = 0
    operator = ""
    if operation == "+":
        port = ADD_PORT
        operator = "SUM"
    elif operation == "-":
        port = SUBTRACT_PORT
        operator = "SUB"
    elif operation == "*":
        port = MULTIPLY_PORT
        operator = "MUL"
    elif operation in ["/", ":"]:
        port = DIVIDE_PORT
        operator = "DIV"

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((HOST, port))
        command = f"{operator} {num1} {num2}".encode()
        client.sendall(command)
        data = client.recv(1024)
        result = float(data.decode())
    
    return result
        

def server_loop():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((HOST, MAIN_PORT))
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

                result = float(tokens[0])
                for i in range(1, len(tokens), 2):
                    operation = tokens[i]
                    num = float(tokens[i + 1])

                    result = calculate_next(result, num, operation)
                
                connection.sendall(bytes(str(result).encode()))


while True:
    server_loop()
