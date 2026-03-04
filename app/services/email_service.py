import os
import requests

def enviar_correo(destinatario, password, folio, app):
    api_key = os.getenv("RESEND_API_KEY")
    if not api_key:
        print("❌ RESEND_API_KEY no está definida, no se enviará el correo")
        return

    payload = {
        "from": "Sistema Aspirantes <onboarding@resend.dev>",
        "to": destinatario,
        "subject": "Clave de acceso y FOLIO - Sistema Aspirantes",
        "html": f"""
        <h2>Bienvenido al Sistema de Aspirantes</h2>
        <p><strong>FOLIO:</strong> {folio}</p>
        <p><strong>Clave:</strong> {password}</p>
        <p>Puedes iniciar sesión en tu sistema.</p>
        """
    }

    # Manejo seguro del request para que no bloquee la app
    try:
        response = requests.post(
            "https://api.resend.com/emails",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=10  # <- muy importante: no deja el thread colgado
        )
        print("Status code:", response.status_code)
        print("Response:", response.text)
    except Exception as e:
        print("Error enviando correo:", e)