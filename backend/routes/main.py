from . import main_bp
from flask import jsonify, render_template, session, redirect, url_for

@main_bp.route("/")
def home():
    return render_template("home.html")

@main_bp.route("/health")
def health():
    return jsonify({"status": "ok"})

@main_bp.route("/map")
def map_view():
    # Ruta para mostrar el formulario y el mapa
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("auth.login"))
    return render_template("frontend.html", user_id=user_id)