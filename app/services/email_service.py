import smtplib
from email.message import EmailMessage
from flask import current_app

def enviar_correo(destinatario, password, folio):
    # Se asume que se llama dentro del contexto de Flask
    msg = EmailMessage()
    msg['Subject'] = 'Clave de acceso y FOLIO - Sistema Aspirantes'
    msg['From'] = current_app.config['MAIL_USERNAME']
    msg['To'] = destinatario

    msg.set_content(f"""
Bienvenido al Sistema de Aspirantes

Su FOLIO de registro es: {folio}
Su clave de acceso es: {password}

Puede iniciar sesión en:
http://127.0.0.1:5000/login

Guarde su folio para cualquier aclaración.
""")

    with smtplib.SMTP(current_app.config['MAIL_SERVER'], current_app.config['MAIL_PORT']) as server:
        server.starttls()
        server.login(current_app.config['MAIL_USERNAME'], current_app.config['MAIL_PASSWORD'])
        server.send_message(msg)