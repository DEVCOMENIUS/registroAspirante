import smtplib
from email.message import EmailMessage
from flask import current_app, Flask

def enviar_correo(destinatario, password, folio, app: Flask):
    """Envía el correo usando el contexto de la app Flask"""
    try:
        # Abrimos el contexto de la app dentro del thread
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

            # Conexión segura a SMTP
            with smtplib.SMTP(current_app.config['MAIL_SERVER'], current_app.config['MAIL_PORT']) as server:
                server.starttls()
                server.login(current_app.config['MAIL_USERNAME'], current_app.config['MAIL_PASSWORD'])
                server.send_message(msg)
                print(f"[INFO] Correo enviado correctamente a {destinatario}")
    except Exception as e:
        print(f"⚠️ Error enviando correo: {e}")