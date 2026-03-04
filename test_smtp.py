import socket

try:
    s = socket.create_connection(("smtp.gmail.com", 587), timeout=10)
    print("Conexión exitosa")
except Exception as e:
    print("Error de conexión:", e)