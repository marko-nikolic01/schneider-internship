import socket

HOST = "127.0.0.1"
PORT = 50000

expression = ""
while True:
    expression = input("Enter your expression (enter 'q' to exit): ")
    if expression == "q":
        break
    if expression == "":
        continue

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((HOST, PORT))
        client.sendall(expression.encode())
        data = client.recv(1024)
        result = data.decode()

    print(f"Result is: {result}")
    print()

print()
print("Finished!")
