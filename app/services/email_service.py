import os
import requests

def enviar_correo(destinatario, password, folio, app):
    try:
        with app.app_context():
            api_key = os.getenv("RESEND_API_KEY")

            response = requests.post(
                "https://api.resend.com/emails",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "from": "Sistema Aspirantes <onboarding@resend.dev>",
                    "to": destinatario,
                    "subject": "Clave de acceso y FOLIO - Sistema Aspirantes",
                    "html": f"""
                    <h2>Bienvenido al Sistema de Aspirantes</h2>
                    <p><strong>FOLIO:</strong> {folio}</p>
                    <p><strong>Clave:</strong> {password}</p>
                    <p>Puedes iniciar sesión en tu sistema.</p>
                    """
                },
            )

            print("Status code:", response.status_code)
            print("Response:", response.text)

    except Exception as e:
        print("Error enviando correo:", e)