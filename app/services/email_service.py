import requests

def enviar_correo(destinatario, password, folio):

    payload = {
        "email": destinatario,
        "subject": "Clave de acceso y FOLIO - Sistema Aspirantes",
        "html": f"""
        <h2>Bienvenido al Sistema de Aspirantes</h2>
        <p><strong>FOLIO:</strong> {folio}</p>
        <p><strong>Clave:</strong> {password}</p>
        """
    }

    try:
        requests.post(
            "https://api-correo-8f7m.onrender.com/enviar",  # <- aquí tu microservicio
            json=payload,
            timeout=60
        )
    except Exception as e:
        print("Error enviando correo:", e)