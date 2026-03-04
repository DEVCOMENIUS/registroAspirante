import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def generar_pdf(aspirante, referencia):
    """
    Genera un PDF con los datos del aspirante y referencia de pago.
    Devuelve la ruta absoluta del PDF generado.
    """

    # Carpeta de PDFs en la raíz del proyecto
    pdf_folder = os.path.abspath(os.path.join(os.getcwd(), 'pdfs'))
    if not os.path.exists(pdf_folder):
        os.makedirs(pdf_folder)

    # Ruta del PDF
    ruta_pdf = os.path.join(pdf_folder, f"solicitud_{aspirante.consecutivo}.pdf")

    # Crear canvas
    c = canvas.Canvas(ruta_pdf, pagesize=letter)

    # Datos principales
    c.drawString(50, 770, f"FOLIO: {aspirante.folio}")
    c.drawString(50, 750, f"Solicitud No: {aspirante.consecutivo}")
    c.drawString(50, 730, f"Nombre: {aspirante.nombre} {aspirante.paterno} {aspirante.materno}")
    c.drawString(50, 710, f"Programa: {aspirante.programa}")
    c.drawString(50, 690, f"CURP: {aspirante.curp}")
    c.drawString(50, 670, f"Referencia BBVA: {referencia}")
    c.drawString(50, 650, "Monto: $500 MXN")

    # Foto (si existe)
    if aspirante.foto and os.path.exists(aspirante.foto):
        try:
            c.drawImage(aspirante.foto, 400, 650, width=120, height=120)
        except Exception:
            pass  # no fallar si la imagen no se carga

    c.save()
    return ruta_pdf