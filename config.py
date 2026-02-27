import os

class Config:
    # ==========================
    # CONFIGURACIÓN GENERAL
    # ==========================
    SECRET_KEY = 'clave_super_segura_local_2026'
    
    # ==========================
    # BASE DE DATOS MYSQL
    # Usuario: root, Password vacío
    # Host: localhost, BD: sistema_aspirantes
    # ==========================
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost/sistema_aspirantes'
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