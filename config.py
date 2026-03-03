import os

class Config:
    # ==========================
    # SEGURIDAD
    # ==========================
    SECRET_KEY = os.getenv("SECRET_KEY", "dev_key_local")

    # ==========================
    # BASE DE DATOS
    # ==========================
    # En Railway usará MYSQL_URL
    # En local usará tu MySQL localhost
    database_url = os.getenv("MYSQL_URL")

    if database_url and database_url.startswith("mysql://"):
        database_url = database_url.replace("mysql://", "mysql+pymysql://", 1)

    SQLALCHEMY_DATABASE_URI = database_url or "mysql+pymysql://root:@localhost/sistema_aspirantes"
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