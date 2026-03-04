from app import db
from datetime import datetime

class Aspirante(db.Model):
    __tablename__ = 'aspirantes'
    
    id = db.Column(db.Integer, primary_key=True)
    folio = db.Column(db.String(20), unique=True, nullable=False)
    consecutivo = db.Column(db.Integer, unique=True)
    nombre = db.Column(db.String(100), nullable=False)
    paterno = db.Column(db.String(100), nullable=False)
    materno = db.Column(db.String(100), nullable=False)
    fecha_nacimiento = db.Column(db.Date, nullable=False)
    sexo = db.Column(db.String(20), nullable=False)
    programa = db.Column(db.String(200), nullable=False)
    curp = db.Column(db.String(20), nullable=False)
    foto = db.Column(db.String(255))
    
    # Relación con Usuario - usa back_populates en lugar de backref
    usuario_rel = db.relationship('Usuario', back_populates='aspirante_rel', uselist=False, lazy=True)
    
    def __repr__(self):
        return f'<Aspirante {self.nombre} {self.paterno}>'