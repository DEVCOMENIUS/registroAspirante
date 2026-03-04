import smtplib
from email.message import EmailMessage
from flask import current_app

def enviar_correo(destinatario, password, folio):
    try:
        msg = EmailMessage()
        msg["Subject"] = "Clave de acceso y FOLIO - Sistema Aspirantes"
        msg["From"] = current_app.config["MAIL_USERNAME"]
        msg["To"] = destinatario

        msg.set_content(f"""
Bienvenido al Sistema de Aspirantes

Su FOLIO de registro es: {folio}
Su clave de acceso es: {password}

Puede iniciar sesión en:
https://TU_DOMINIO.up.railway.app/login
""")

        with smtplib.SMTP(
            current_app.config["MAIL_SERVER"],
            current_app.config["MAIL_PORT"],
            timeout=10  # 🔥 evita que se congele
        ) as server:

            if current_app.config["MAIL_USE_TLS"]:
                server.starttls()

            server.login(
                current_app.config["MAIL_USERNAME"],
                current_app.config["MAIL_PASSWORD"]
            )

            server.send_message(msg)

    except Exception as e:
        print("⚠️ Error enviando correo:", e)