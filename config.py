import os

class Config:
    # ==========================
    # SEGURIDAD
    # ==========================
    SECRET_KEY = os.getenv("SECRET_KEY", "dev_key_local")

    # ==========================
    # BASE DE DATOS
    # ==========================
    # Para Railway: usa MYSQL_URL o construye la URL con las variables individuales
    mysql_url = os.getenv("MYSQL_URL")  # Railway shared variable
    db_user = os.getenv("DB_USER", "root")
    db_password = os.getenv("DB_PASSWORD", "")
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = os.getenv("DB_PORT", "3306")
    db_name = os.getenv("DB_NAME", "sistema_aspirantes")

    if mysql_url and mysql_url.startswith("mysql://"):
        # Convierte la URL de Railway para pymysql
        SQLALCHEMY_DATABASE_URI = mysql_url.replace("mysql://", "mysql+pymysql://", 1)
    else:
        # Conexión local o con variables individuales
        SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}?allowPublicKeyRetrieval=true&sslMode=DISABLED"

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ==========================
    # CONFIGURACIÓN DE CORREO (GMAIL)
    # IMPORTANTE: usar contraseña de aplicación
    # ==========================
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'fernanda.agustin1123@gmail.com'      # ← CAMBIA ESTO por tu correo real
    MAIL_PASSWORD = 'webo iuhh sgqa obop'          # ← CAMBIA ESTO por contraseña de aplicacióna