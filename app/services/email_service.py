import smtplib
from email.message import EmailMessage

def enviar_correo(destinatario, password, folio, config):
    """
    Envía correo usando configuración pasada como diccionario para threads.
    """
    msg = EmailMessage()
    msg["Subject"] = "Clave de acceso y FOLIO - Sistema Aspirantes"
    msg["From"] = config["MAIL_USERNAME"]
    msg["To"] = destinatario

    msg.set_content(f"""
Bienvenido al Sistema de Aspirantes

Su FOLIO de registro es: {folio}
Su clave de acceso es: {password}

Puede iniciar sesión en:
https://TU_DOMINIO.up.railway.app/login

Guarde su folio para cualquier aclaración.
""")

    with smtplib.SMTP(config["MAIL_SERVER"], config["MAIL_PORT"], timeout=10) as server:
        if config["MAIL_USE_TLS"]:
            server.starttls()
        server.login(config["MAIL_USERNAME"], config["MAIL_PASSWORD"])
        server.send_message(msg)