import smtplib
from email.message import EmailMessage
from flask import current_app, Flask

def enviar_correo(destinatario, password, folio, app: Flask):
    """Envía correo usando SMTP SSL y contexto de Flask"""
    try:
        with app.app_context():
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
            print(f"[INFO] Intentando enviar correo a {destinatario}...")

            # SMTP SSL (puerto 465) en vez de TLS
            with smtplib.SMTP_SSL(current_app.config['MAIL_SERVER'], 465) as server:
                server.login(current_app.config['MAIL_USERNAME'], current_app.config['MAIL_PASSWORD'])
                server.send_message(msg)
                print(f"[INFO] Correo enviado correctamente a {destinatario}")
    except Exception as e:
        print(f"⚠️ Error enviando correo: {e}")