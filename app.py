import os
import random
import string
from datetime import datetime
from io import BytesIO
import base64

from flask import Flask, render_template, request, redirect, url_for, send_file, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import smtplib
from email.message import EmailMessage
from werkzeug.utils import secure_filename
from PIL import Image

from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"

# =====================
# MODELOS
# =====================

class Aspirante(db.Model):
    __tablename__ = 'aspirantes'
    id = db.Column(db.Integer, primary_key=True)
    consecutivo = db.Column(db.Integer, unique=True)
    folio = db.Column(db.String(20), unique=True)  # ← NUEVO CAMPO DE FOLIO
    nombre = db.Column(db.String(100))
    paterno = db.Column(db.String(100))
    materno = db.Column(db.String(100))
    fecha_nacimiento = db.Column(db.Date)
    sexo = db.Column(db.String(20))
    programa = db.Column(db.String(200))
    curp = db.Column(db.String(20))
    foto = db.Column(db.String(255))

class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    aspirante_id = db.Column(db.Integer, db.ForeignKey('aspirantes.id'))
    correo = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(255))
    activo = db.Column(db.Boolean, default=True)

class Pago(db.Model):
    __tablename__ = 'pagos'
    id = db.Column(db.Integer, primary_key=True)
    aspirante_id = db.Column(db.Integer, db.ForeignKey('aspirantes.id'))
    referencia = db.Column(db.String(50))
    monto = db.Column(db.Numeric(10,2))
    estatus = db.Column(db.String(20), default='Pendiente')

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

# =====================
# FUNCIONES AUXILIARES
# =====================

def generar_consecutivo():
    ultimo = db.session.query(db.func.max(Aspirante.consecutivo)).scalar()
    return 1000 if not ultimo else ultimo + 1

def generar_folio():
    """Genera un folio aleatorio de 8 caracteres alfanuméricos"""
    while True:
        # Formato: 2 letras + 4 números + 2 letras (ej: AB1234CD)
        letras1 = ''.join(random.choices(string.ascii_uppercase, k=2))
        numeros = ''.join(random.choices(string.digits, k=4))
        letras2 = ''.join(random.choices(string.ascii_uppercase, k=2))
        folio = f"{letras1}{numeros}{letras2}"
        
        # Verificar que no exista (por si acaso)
        existe = Aspirante.query.filter_by(folio=folio).first()
        if not existe:
            return folio

def generar_password():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))

def generar_referencia(consecutivo):
    return f"BBVA{datetime.now().year}{consecutivo}"

def enviar_correo(destinatario, password, folio):  # ← AGREGADO FOLIO COMO PARÁMETRO
    msg = EmailMessage()
    msg['Subject'] = 'Clave de acceso y FOLIO - Sistema Aspirantes'
    msg['From'] = app.config['MAIL_USERNAME']
    msg['To'] = destinatario

    msg.set_content(f"""
Bienvenido al Sistema de Aspirantes

Su FOLIO de registro es: {folio}
Su clave de acceso es: {password}

Puede iniciar sesión en:
http://127.0.0.1:5000/login

Guarde su folio para cualquier aclaración.
""")

    with smtplib.SMTP(app.config['MAIL_SERVER'], app.config['MAIL_PORT']) as server:
        server.starttls()
        server.login(app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        server.send_message(msg)

def generar_pdf(aspirante, referencia):
    if not os.path.exists("pdfs"):
        os.makedirs("pdfs")

    ruta_pdf = f"pdfs/solicitud_{aspirante.consecutivo}.pdf"
    c = canvas.Canvas(ruta_pdf, pagesize=letter)

    c.drawString(50, 770, f"FOLIO: {aspirante.folio}")  # ← AGREGADO FOLIO AL PDF
    c.drawString(50, 750, f"Solicitud No: {aspirante.consecutivo}")
    c.drawString(50, 730, f"Nombre: {aspirante.nombre} {aspirante.paterno} {aspirante.materno}")
    c.drawString(50, 710, f"Programa: {aspirante.programa}")
    c.drawString(50, 690, f"CURP: {aspirante.curp}")
    c.drawString(50, 670, f"Referencia BBVA: {referencia}")
    c.drawString(50, 650, "Monto: $500 MXN")

    if aspirante.foto and os.path.exists(aspirante.foto):
        c.drawImage(aspirante.foto, 400, 650, width=120, height=120)

    c.save()
    return ruta_pdf

# =====================
# RUTA REGISTRO (MODIFICADA CON FOLIO)
# =====================

@app.route('/', methods=['GET','POST'])
def registro():
    if request.method == 'POST':

        correo = request.form['correo']
        correo_confirm = request.form.get('correo_confirm','')

        if correo != correo_confirm:
            flash("Los correos no coinciden.", "danger")
            return redirect(url_for('registro'))

        consecutivo = generar_consecutivo()
        folio = generar_folio()  # ← GENERAR FOLIO ALEATORIO
        password = generar_password()

        carpeta_fotos = "static/fotos"
        if not os.path.exists(carpeta_fotos):
            os.makedirs(carpeta_fotos)

        ruta_foto = os.path.join(carpeta_fotos, f"{consecutivo}_foto.png")

        preview_base64 = request.form.get('preview_base64')

        # FOTO BASE64
        if preview_base64 and ',' in preview_base64:
            try:
                encoded_data = preview_base64.split(',')[1]
                img_data = base64.b64decode(encoded_data)
                img = Image.open(BytesIO(img_data))
                img = img.convert("RGB")
                img.save(ruta_foto, format="PNG")
            except Exception as e:
                print("Error base64:", e)
                flash("Error al procesar la foto tomada.", "danger")
                return redirect(url_for('registro'))

        # FOTO ARCHIVO
        elif 'foto' in request.files and request.files['foto'].filename != '':
            foto_file = request.files['foto']
            filename = secure_filename(foto_file.filename)

            allowed_extensions = {'png','jpg','jpeg'}
            if '.' not in filename:
                flash("Archivo inválido.", "danger")
                return redirect(url_for('registro'))

            ext = filename.rsplit('.',1)[1].lower()
            if ext not in allowed_extensions:
                flash("Solo PNG, JPG o JPEG.", "danger")
                return redirect(url_for('registro'))

            try:
                img = Image.open(foto_file)
                img = img.convert("RGB")
                img.save(ruta_foto, format="PNG")
            except Exception as e:
                print("Error imagen:", e)
                flash("Imagen no válida.", "danger")
                return redirect(url_for('registro'))
        else:
            flash("Debe subir o tomar una foto.", "danger")
            return redirect(url_for('registro'))

        fecha_convertida = datetime.strptime(request.form['fecha'], "%Y-%m-%d").date()

        # IMPORTANTE: Usando los nombres correctos del HTML
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

        # CREAR USUARIO
        hash_pw = bcrypt.generate_password_hash(password).decode('utf-8')
        usuario = Usuario(
            aspirante_id=aspirante.id,
            correo=correo,
            password_hash=hash_pw
        )

        # CREAR PAGO
        referencia = generar_referencia(consecutivo)
        pago = Pago(
            aspirante_id=aspirante.id,
            referencia=referencia,
            monto=500.00
        )

        db.session.add(usuario)
        db.session.add(pago)
        db.session.commit()

        # ENVIAR CORREO CON FOLIO Y CONTRASEÑA
        enviar_correo(correo, password, folio)  # ← PASAR FOLIO A LA FUNCIÓN

        pdf_path = generar_pdf(aspirante, referencia)

        return send_file(pdf_path, as_attachment=True)

    return render_template("registro.html")

# =====================
# VER PDF (EN NAVEGADOR)
# =====================
@app.route('/ver_pdf')
@login_required
def ver_pdf():
    aspirante = Aspirante.query.filter_by(id=current_user.aspirante_id).first()
    if not aspirante:
        flash("No se encontró el aspirante.", "danger")
        return redirect(url_for('dashboard'))

    referencia = generar_referencia(aspirante.consecutivo)
    pdf_path = generar_pdf(aspirante, referencia)

    return send_file(pdf_path, as_attachment=False)


# =====================
# DESCARGAR PDF
# =====================
@app.route('/descargar_pdf')
@login_required
def descargar_pdf():
    aspirante = Aspirante.query.filter_by(id=current_user.aspirante_id).first()
    if not aspirante:
        flash("No se encontró el aspirante.", "danger")
        return redirect(url_for('dashboard'))

    referencia = generar_referencia(aspirante.consecutivo)
    pdf_path = generar_pdf(aspirante, referencia)

    return send_file(
        pdf_path,
        as_attachment=True,
        download_name=f"Ficha_{aspirante.folio}.pdf"
    )

# =====================
# LOGIN
# =====================

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        user = Usuario.query.filter_by(correo=request.form['correo']).first()
        if user and bcrypt.check_password_hash(user.password_hash, request.form['password']):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash("Credenciales incorrectas", "danger")
    return render_template("login.html")

@app.route('/dashboard')
@login_required
def dashboard():
    # OPCIONAL: Mostrar el folio del aspirante en el dashboard
    aspirante = Aspirante.query.filter_by(id=current_user.aspirante_id).first()
    return render_template("dashboard.html", aspirante=aspirante)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)