# email_service.py
import smtplib
from email.message import EmailMessage
from flask import current_app

def enviar_correo(destinatario, password, folio):
    try:
        # Obtener el objeto app real
        app = current_app._get_current_object()

        # Crear contexto de aplicación dentro del thread
        with app.app_context():
            msg = EmailMessage()
            msg["Subject"] = "Clave de acceso y FOLIO - Sistema Aspirantes"
            msg["From"] = app.config["MAIL_USERNAME"]
            msg["To"] = destinatario

            msg.set_content(f"""
Bienvenido al Sistema de Aspirantes

Su FOLIO de registro es: {folio}
Su clave de acceso es: {password}

Puede iniciar sesión en:
https://TU_DOMINIO.up.railway.app/login
""")

            with smtplib.SMTP(app.config["MAIL_SERVER"], app.config["MAIL_PORT"], timeout=10) as server:
                if app.config["MAIL_USE_TLS"]:
                    server.starttls()
                server.login(app.config["MAIL_USERNAME"], app.config["MAIL_PASSWORD"])
                server.send_message(msg)

    except Exception as e:
        print("⚠️ Error enviando correo:", e)