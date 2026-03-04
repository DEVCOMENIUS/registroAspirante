import os
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )

    import socket

try:
    s = socket.create_connection(("smtp.gmail.com", 587), timeout=10)
    print("Conexión exitosa")
except Exception as e:
    print("Error de conexión:", e)