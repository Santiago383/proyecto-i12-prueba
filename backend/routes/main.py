from . import main_bp
from flask import jsonify, render_template

@main_bp.route("/")
def home():
    return jsonify({"message": "Bienvenido a la API 🚀"})

@main_bp.route("/health")
def health():
    return jsonify({"status": "ok"})

@main_bp.route("/map")
def map_view():
    # Ruta para mostrar el formulario y el mapa
    return render_template("frontend.html")