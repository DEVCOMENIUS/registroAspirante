import smtplib
from email.message import EmailMessage

EMAIL = 'fernanda.agustin1123@gmail.com'
PASS = 'webo iuhh sgqa obop'  # contraseña de aplicación exacta

msg = EmailMessage()
msg['Subject'] = 'Prueba'
msg['From'] = EMAIL
msg['To'] = EMAIL  # prueba enviando a ti mismo
msg.set_content('Esto es una prueba de envío de correo desde Python')

try:
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(EMAIL, PASS)
        server.send_message(msg)
        print("Correo enviado correctamente")
except Exception as e:
    print("Error:", e)