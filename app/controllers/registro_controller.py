import os
import threading
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file, current_app
from app import db, bcrypt
from app.models.aspirante import Aspirante
from app.models.usuario import Usuario
from app.models.pago import Pago
from app.utils.helpers import (
    generar_consecutivo,
    generar_folio,
    generar_password,
    generar_referencia
)
from app.services.email_service import enviar_correo
from app.services.file_service import (
    procesar_foto_base64,
    procesar_foto_archivo,
    crear_carpeta_si_no_existe
)
from app.services.pdf_service import generar_pdf
from sqlalchemy.exc import IntegrityError

registro_bp = Blueprint('registro', __name__)

@registro_bp.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        correo = request.form['correo']
        correo_confirm = request.form.get('correo_confirm', '')

        # 🔹 Validar que los correos coincidan
        if correo != correo_confirm:
            flash("Los correos no coinciden.", "danger")
            return redirect(url_for('registro.registro'))

        # 🔹 Validar que el correo no exista
        if Usuario.query.filter_by(correo=correo).first():
            flash("Este correo ya está registrado.", "danger")
            return redirect(url_for('registro.registro'))

        # 🔹 Generación de datos
        consecutivo = generar_consecutivo()
        folio = generar_folio()
        password = generar_password()

        # 🔹 Manejo de foto
        carpeta_fotos = "static/fotos"
        crear_carpeta_si_no_existe(carpeta_fotos)
        ruta_foto = os.path.join(carpeta_fotos, f"{consecutivo}_foto.png")

        preview_base64 = request.form.get('preview_base64')
        foto_file = request.files.get('foto')

        foto_procesada = False
        if preview_base64:
            foto_procesada = procesar_foto_base64(preview_base64, ruta_foto)
        elif foto_file and foto_file.filename != '':
            foto_procesada = procesar_foto_archivo(foto_file, ruta_foto)

        if not foto_procesada:
            flash("Debe subir o tomar una foto válida.", "danger")
            return redirect(url_for('registro.registro'))

        # 🔹 Convertir fecha
        fecha_convertida = datetime.strptime(request.form['fecha'], "%Y-%m-%d").date()

        # 🔹 Crear Aspirante
        aspirante = Aspirante(
            consecutivo=consecutivo,
            folio=folio,
            nombre=request.form['nombre'],
            paterno=request.form['paterno'],
            materno=request.form['materno'],
            fecha_nacimiento=fecha_convertida,
            sexo=request.form['sexo'],
            programa=request.form['programa'],
            curp=request.form['curp'],
            foto=ruta_foto
        )

        db.session.add(aspirante)
        db.session.commit()

        # 🔹 Crear Usuario
        hash_pw = bcrypt.generate_password_hash(password).decode('utf-8')
        usuario = Usuario(
            aspirante_id=aspirante.id,
            correo=correo,
            password_hash=hash_pw
        )

        # 🔹 Crear Pago
        referencia = generar_referencia(consecutivo)
        pago = Pago(
            aspirante_id=aspirante.id,
            referencia=referencia,
            monto=500.00
        )

        db.session.add(usuario)
        db.session.add(pago)

        # 🔹 Commit con manejo de duplicados por seguridad
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash("El correo ya está registrado.", "danger")
            return redirect(url_for('registro.registro'))

        # 🔹 Enviar correo en segundo plano con contexto de Flask
        def enviar_correo_thread():
            try:
                app = current_app._get_current_object()
                with app.app_context():
                    enviar_correo(correo, password, folio)
            except Exception as e:
                print("⚠️ Error enviando correo:", e)

        threading.Thread(target=enviar_correo_thread, daemon=True).start()

        # 🔹 Crear carpeta PDFs si no existe
        pdf_folder = "app/pdfs"
        if not os.path.exists(pdf_folder):
            os.makedirs(pdf_folder)

        # 🔹 Generar PDF
        pdf_path = generar_pdf(aspirante, referencia, output_folder=pdf_folder)

        if not os.path.exists(pdf_path):
            flash("Error generando el PDF.", "danger")
            return redirect(url_for('registro.registro'))

        return send_file(pdf_path, as_attachment=True)

    return render_template("registro.html")