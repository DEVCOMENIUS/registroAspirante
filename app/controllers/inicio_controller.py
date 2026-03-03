# app/controllers/inicio_controller.py
from flask import Blueprint, render_template

inicio_bp = Blueprint('inicio', __name__)

@inicio_bp.route('/')
def index():
    """Página principal del sistema"""
    return render_template('index.html')